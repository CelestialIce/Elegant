import tkinter as tk
from tkinter import messagebox
import requests
from lxml import etree
import json

#哈哈哈
#插件使用

#哥们又切换回主支了
#天下无敌

#关于自己iss53的修改

class PoemDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("古籍下载器")
        self.root.geometry("1000x800")  # 修改窗口大小

        self.base_url = 'https://www.gushici.net/book/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.86'
        }

        self.downloaded_poems_file = 'downloaded_poems.txt'
        self.downloaded_poems = self.read_downloaded_poems()
        if not self.load_data_from_file():
            self.all_poem_names, self.all_poem_links = self.fetch_all_poems()
            self.save_data_to_file()

        self.poem_list_var = tk.StringVar(self.root)
        self.poem_list_var.set(())
        self.poem_list_label = tk.Label(self.root, text="The following are ancient books that can be crawled(Scroll up and down to discover new books)")
        self.poem_list_label.grid(row=0, column=0, padx=10, pady=5)
        self.poem_list = tk.Listbox(self.root, listvariable=self.poem_list_var, selectmode=tk.SINGLE, height=20, width=50)
        self.poem_list.grid(row=1, column=0, padx=10, pady=5)

        self.progress_label = tk.Label(self.root, text="download progress:")
        self.progress_label.grid(row=0, column=1, padx=10, pady=5)

        self.progress_listbox = tk.Listbox(self.root, height=20, width=50)
        self.progress_listbox.grid(row=1, column=1, padx=10, pady=10)

        self.prompt_label = tk.Label(self.root, text="Which one do you want to download (Names:)Please enter in the box on the right--->")
        self.prompt_label.grid(row=2, column=0, padx=10, pady=5)

        self.poem_input_var = tk.StringVar(self.root)
        self.poem_input = tk.Entry(self.root, textvariable=self.poem_input_var, width=50)
        self.poem_input.grid(row=2, column=1, padx=10, pady=5)

        self.download_button = tk.Button(self.root, text="下载", command=self.download_poem)
        self.download_button.grid(row=3, column=0, padx=10, pady=5)

        self.update_button = tk.Button(self.root, text="刷新列表", command=self.update_poem_list)
        self.update_button.grid(row=3, column=1, padx=10, pady=5)

        self.downloaded_label = tk.Label(self.root, text="Downloaded books")
        self.downloaded_label.grid(row=4, column=0, padx=10, pady=5)

        self.downloaded_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=50)
        self.downloaded_listbox.grid(row=5, column=0, padx=10, pady=5)

        self.update_poem_list()
        self.update_downloaded_list()

    def refresh_lists_periodically(self):
        # 刷新已下载列表
        self.update_downloaded_list()
        # 设置定时器，每隔一段时间自动刷新列表
        self.root.after(10000, self.refresh_lists_periodically) 

    def update_downloaded_list(self):
        self.downloaded_listbox.delete(0, tk.END)
        for book in self.downloaded_poems:
            self.downloaded_listbox.insert(tk.END, book)
    
    def fetch_page_content(self, url):
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            encoding = response.apparent_encoding
            response.encoding = encoding
            return response.text
        else:
            return None
    def load_data_from_file(self):
        # 尝试从文件中加载数据
        try:
            with open("poem_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.all_poem_names = data["poem_names"]
                self.all_poem_links = data["poem_links"]
                return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False

    def save_data_to_file(self):
        # 将数据保存到文件中
        data = {
            "poem_names": self.all_poem_names,
            "poem_links": self.all_poem_links
        }
        with open("poem_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    def fetch_all_poems(self):
        all_poem_names = []
        all_poem_links = []

        response_text = self.fetch_page_content(self.base_url + 'index.html')
        if response_text is not None:
            tree = etree.HTML(response_text)
            anchor_elements = tree.xpath('//a[@style="font-size:18px; line-height:22px; height:22px;"]/b')

            for anchor_element in anchor_elements:
                poem_name = anchor_element.text
                poem_link = anchor_element.xpath('../@href')[0]
                poem_name = poem_name  # 不再转换编码
                all_poem_names.append(poem_name)
                all_poem_links.append('https://www.gushici.net' + poem_link)

        for page_num in range(2, 38):  # Page numbers range from 2 to 37
            url = f'{self.base_url}index_{page_num}.html'
            response_text = self.fetch_page_content(url)
            if response_text is not None:
                tree = etree.HTML(response_text)
                anchor_elements = tree.xpath('//a[@style="font-size:18px; line-height:22px; height:22px;"]/b')

                for anchor_element in anchor_elements:
                    poem_name = anchor_element.text
                    poem_link = anchor_element.xpath('../@href')[0]
                    poem_name = poem_name  # 不再转换编码
                    all_poem_names.append(poem_name)
                    all_poem_links.append('https://www.gushici.net' + poem_link)

        return all_poem_names, all_poem_links

    def extract_info_from_poem_html(self, html):
        tree = etree.HTML(html)
        poem_names = tree.xpath('//a[@href]/text()')
        poem_links = tree.xpath('//a[@href]/@href')
        return poem_names, poem_links

    def write_to_txt_file(self, query, poem_name, poem_content):
        file_name = query + '.txt'

        with open(file_name, 'ab') as file:
            names_line = ''.join(poem_name) + '\n'
            file.write(names_line.encode('utf-8'))

            # Write the poem content from <p> tags
            tree = etree.HTML(poem_content)
            p_tags = tree.xpath('//div[@class="shici-box-text"]/p')
            p_texts = [p.text.strip() for p in p_tags if p.text is not None]
            p_texts_lines = '\n' + '\n'.join(p_texts) + '\n' + '\n'
            
            if p_texts_lines.strip():  # Check if p_texts_lines is not empty before writing
                file.write(p_texts_lines.encode('utf-8'))

            # Write the text content from the <div class="shici-box-text"> itself
            div_text = tree.xpath('//div[@class="shici-box-text"]/text()')
            div_text = ''.join(div_text).strip()
            div_text_lines = '\n' + div_text + '\n' + '\n'

            if div_text_lines.strip():  # Check if div_text_lines is not empty before writing
                file.write(div_text_lines.encode('utf-8'))

        # 输出下载进度信息
        self.progress_listbox.insert(tk.END, f"{poem_name} has been downloaded into: {file_name}")


    def read_downloaded_poems(self):
        try:
            with open(self.downloaded_poems_file, 'r', encoding='utf-8') as file:
                return set(file.read().splitlines())
        except FileNotFoundError:
            return set()

    def save_downloaded_poems(self):
        with open(self.downloaded_poems_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(self.downloaded_poems))

    def download_poem(self):
        selected_poem = self.poem_input_var.get()

        if not selected_poem:
            messagebox.showwarning("警告", "请选择要下载的诗歌。")
            return

        if selected_poem in self.downloaded_poems:
            messagebox.showinfo("提示", f"{selected_poem} 已经下载过。")
            return

        if selected_poem not in self.all_poem_names:
            messagebox.showerror("错误", "未找到该诗歌名称。")
            return

        index = self.all_poem_names.index(selected_poem)
        if index < len(self.all_poem_links):
            poem_url = self.all_poem_links[index]
            new_response_text = self.fetch_page_content(poem_url)
            if new_response_text:
                new_poem_names, new_poem_links = self.extract_info_from_poem_html(new_response_text)
                new_poem_links_with_prefix = ['https://www.gushici.net/' + link for link in new_poem_links[1:]]
                poem_name_link_dict = dict(zip(new_poem_names, new_poem_links_with_prefix))
                filtered_poem_names = [name for name in new_poem_names if name not in ['古诗词网', '首页', '诗词', '名句', '作者', '古籍', '分类', '手机版', '古诗词网', '免责声明', '鲁ICP备20001911号-1']]

                if filtered_poem_names:
                    filtered_poem_links = [poem_name_link_dict.get(name, "Link not found") for name in filtered_poem_names]
                    for filtered_link, name in zip(filtered_poem_links, filtered_poem_names):
                        html_content = self.fetch_page_content(filtered_link)
                        if html_content:
                            self.write_to_txt_file(selected_poem,name, html_content)
                    self.downloaded_poems.add(selected_poem)
                    self.save_downloaded_poems()
                    messagebox.showinfo("成功", f"{selected_poem} 下载完成！")
                else:
                    messagebox.showwarning("警告", "该诗歌没有附加信息。")
            else:
                messagebox.showerror("错误", "获取附加信息失败。")
        else:
            messagebox.showerror("错误", "未找到诗歌链接。")

    def update_poem_list(self):
        all_poem_names, all_poem_links = self.fetch_all_poems()
        if not all_poem_names:
            messagebox.showwarning("警告", "没有找到可用的诗歌。")
            return
        self.all_poem_names = all_poem_names
        self.all_poem_links = all_poem_links
        self.poem_list_var.set(tuple(all_poem_names))
        self.poem_input_var.set('')  # 清空输入框

    def update_downloaded_list(self):
        self.downloaded_listbox.delete(0, tk.END)
        for book in self.downloaded_poems:
            self.downloaded_listbox.insert(tk.END, book)

if __name__ == "__main__":
    root = tk.Tk()
    app = PoemDownloaderApp(root)
    app.refresh_lists_periodically()  # 开始定时刷新列表
    root.mainloop()
