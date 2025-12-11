from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import io

app = Flask(__name__)

columns = ["Name", "ContactMethods", "IsFavorite"]
data = pd.DataFrame(columns=columns)


@app.route('/')
def index():
    global data
    filter_type = request.args.get('filter')
    df_display = data.copy()

    if filter_type == 'fav':
        df_display = df_display[df_display['IsFavorite'] == True]

    if not df_display.empty:
        df_sorted = df_display.sort_values(by="IsFavorite", ascending=False)
    else:
        df_sorted = df_display

    contacts = df_sorted.to_dict(orient='records')
    for i, contact in enumerate(contacts):
        contact['id'] = df_sorted.index[i]
    return render_template('index.html', contacts=contacts, current_filter=filter_type)


@app.route('/add', methods=['POST'])
def add_contact():
    global data
    name = request.form.get('name')
    methods = request.form.get('methods')
    new_row = {"Name": name, "ContactMethods": methods, "IsFavorite": False}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    return redirect(url_for('index'))


@app.route('/toggle_fav/<int:idx>')
def toggle_fav(idx):
    global data
    data.at[idx, "IsFavorite"] = not data.at[idx, "IsFavorite"]
    filter_type = request.args.get('filter')
    if filter_type == 'fav':
        return redirect(url_for('index', filter='fav'))
    return redirect(url_for('index'))


@app.route('/delete/<int:idx>')
def delete_contact(idx):
    global data
    data = data.drop(idx).reset_index(drop=True)
    return redirect(url_for('index'))


@app.route('/export')
def export_excel():
    global data

    export_list = []

    for _, row in data.iterrows():
        # 基础信息
        row_dict = {
            'Name': row['Name'],
            'IsFavorite': "Yes" if row['IsFavorite'] else "No"  # 导出时变成 Yes/No 更好看
        }

        # 解析 ContactMethods (例如 "Mobile:123;Email:abc")
        methods_str = str(row['ContactMethods']) if pd.notna(row['ContactMethods']) else ""
        if methods_str:
            parts = methods_str.split(';')
            for part in parts:
                if ':' in part:
                    # 拆分类型和值
                    m_type, m_val = part.split(':', 1)
                    m_type = m_type.strip()  # 去除空格
                    m_val = m_val.strip()

                    # 如果这个人有两个手机号，用逗号拼接 (123, 456)
                    if m_type in row_dict:
                        row_dict[m_type] += f", {m_val}"
                    else:
                        row_dict[m_type] = m_val

        export_list.append(row_dict)

    # 2. 生成 DataFrame
    if not export_list:
        # 如果没数据，至少保证有表头
        df_export = pd.DataFrame(columns=['Name', 'IsFavorite', 'Mobile', 'Email'])
    else:
        df_export = pd.DataFrame(export_list)

    # 3. 整理列顺序：Name, IsFavorite 在前，其他列 (Mobile, Email...) 在后
    cols = list(df_export.columns)
    if 'Name' in cols: cols.remove('Name')
    if 'IsFavorite' in cols: cols.remove('IsFavorite')
    # 剩下的列按字母排序 (Email, Mobile, WeChat...)
    final_cols = ['Name', 'IsFavorite'] + sorted(cols)
    df_export = df_export[final_cols]

    # 4. 导出
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False)
    output.seek(0)

    return send_file(output, download_name="contacts_separated.xlsx", as_attachment=True)


@app.route('/import', methods=['POST'])
def import_excel():
    global data
    file = request.files['file']
    if file:
        try:
            # 1. 读取 Excel
            df_input = pd.read_excel(file)

            # 2. 准备转换回来的列表
            new_rows = []

            for _, row in df_input.iterrows():
                name = row.get('Name', 'Unknown')

                # 处理收藏状态
                fav_raw = str(row.get('IsFavorite', 'No')).lower()
                is_fav = True if fav_raw in ['yes', 'true', '1'] else False

                # 处理联系方式：遍历所有不是 Name 和 IsFavorite 的列
                methods_list = []
                for col in df_input.columns:
                    if col not in ['Name', 'IsFavorite']:
                        val = row[col]
                        # 如果这一格有值 (不是 NaN)
                        if pd.notna(val) and str(val).strip() != "":
                            methods_list.append(f"{col}:{val}")

                # 拼成字符串 "Mobile:123;Email:abc"
                methods_str = ";".join(methods_list)

                new_rows.append({
                    "Name": name,
                    "ContactMethods": methods_str,
                    "IsFavorite": is_fav
                })

            # 3. 创建新 DataFrame 并追加 (Append)
            if new_rows:
                new_data = pd.DataFrame(new_rows)
                data = pd.concat([data, new_data], ignore_index=True)

        except Exception as e:
            print(f"Import Error: {e}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
