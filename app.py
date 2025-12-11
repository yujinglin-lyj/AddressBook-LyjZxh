from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import io

app = Flask(__name__)

columns = ["Name", "ContactMethods", "IsFavorite"]
data = pd.DataFrame(columns=columns)


@app.route('/')
def index():
    global data

    # 1. 获取 URL 里的参数 (例如 ?filter=fav)
    filter_type = request.args.get('filter')

    # 2. 准备要显示的数据 (使用 copy 防止影响原始数据)
    df_display = data.copy()

    # 3. 如果用户点了 "Show Favorites Only"
    if filter_type == 'fav':
        # 筛选 IsFavorite 为 True 的行
        df_display = df_display[df_display['IsFavorite'] == True]

    # 4. 排序：收藏的依然排在前面（虽然如果是纯收藏列表，这步没啥大变化，但保持逻辑一致）
    if not df_display.empty:
        df_sorted = df_display.sort_values(by="IsFavorite", ascending=False)
    else:
        df_sorted = df_display

    # 5. 转为字典列表传给页面
    contacts = df_sorted.to_dict(orient='records')

    # 6. 把原始的索引 (Index) 放进去，确保删除/修改时 ID 是对的
    for i, contact in enumerate(contacts):
        contact['id'] = df_sorted.index[i]

    # 传参给前端：contacts 数据，以及当前的 filter 状态（用于控制按钮显示）
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
    # 切换状态
    data.at[idx, "IsFavorite"] = not data.at[idx, "IsFavorite"]

    # 核心修改：读取 URL 参数，决定跳回哪里
    filter_type = request.args.get('filter')
    if filter_type == 'fav':
        return redirect(url_for('index', filter='fav'))
    else:
        return redirect(url_for('index'))


@app.route('/delete/<int:idx>')
def delete_contact(idx):
    global data
    data = data.drop(idx).reset_index(drop=True)
    return redirect(url_for('index'))


@app.route('/export')
def export_excel():
    global data
    # 创建内存中的 Excel 文件
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name="contacts.xlsx", as_attachment=True)


@app.route('/import', methods=['POST'])
def import_excel():
    global data
    file = request.files['file']
    if file:
        try:
            new_data = pd.read_excel(file)
            # 数据清洗：处理一下 IsFavorite 列，防止格式报错
            if "IsFavorite" not in new_data.columns:
                new_data["IsFavorite"] = False
            else:
                # 兼容 Excel 里写 "Yes/No" 或 TRUE/FALSE 的情况
                new_data["IsFavorite"] = new_data["IsFavorite"].apply(
                    lambda x: True if str(x).lower() in ['true', 'yes', '1'] else False)

            data = pd.concat([data, new_data], ignore_index=True)
            # --------------------

        except Exception as e:
            print(f"Error: {e}")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
