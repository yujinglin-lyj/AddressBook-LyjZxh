from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import io

app = Flask(__name__)

columns = ["Name", "ContactMethods", "IsFavorite"]
data = pd.DataFrame(columns=columns)


@app.route('/')
def index():
    global data
    # 排序：收藏的在前面
    df_sorted = data.sort_values(by="IsFavorite", ascending=False)
    # 转为字典列表传给页面
    contacts = df_sorted.to_dict(orient='records')
    # 为了方便通过索引操作，我们需要保留原始索引
    for i, contact in enumerate(contacts):
        contact['id'] = df_sorted.index[i]
    return render_template('index.html', contacts=contacts)


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

