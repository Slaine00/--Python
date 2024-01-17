import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog

class MyFrame(tk.Frame):
    """tk.Frame　を継承する、 tkinter を用いた簡単なテキストエディタのためのクラス。
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Simple Editor")

        # メニューの作成　menubar -> filemenu -> Open, Save as, Exit
        menubar = tk.Menu(self)
        
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openfile)
        filemenu.add_command(label="Save as...", command=self.saveas)
        filemenu.add_command(label="Exit", command=self.master.destroy)
        
        menubar.add_cascade(label="File", menu=filemenu)
        self.master.config(menu=menubar)

        # 編集用 Text ウィジェットをクラス変数 editbox として作成
        self.editbox = tk.Text(self)
        self.editbox.pack()

    def openfile(self):
        """ファイルを開くメソッド"""
        filename = tkinter.filedialog.askopenfilename()

        if filename:
            tkinter.messagebox.showinfo("Filename", "Open: " + filename)
            with open(filename, 'r', encoding="utf-8") as file:
                text = file.read()
                
            # ファイル内容を editbox に設定
            self.editbox.delete('1.0', tk.END)
            self.editbox.insert('1.0', text)

        else:
            tkinter.messagebox.showinfo("Filename", "Cancelled")

    def saveas(self):
        """ファイルに保存するメソッド"""
        filename = tkinter.filedialog.asksaveasfilename()
        
        if filename:
            with open(filename, 'w', encoding="utf-8") as file:
                file.write(self.editbox.get('1.0', tk.END))

            tkinter.messagebox.showinfo("Filename", "Saved AS: " + filename)

        else:
            tkinter.messagebox.showinfo("Filename", "Cancelled")

# 実行
root = tk.Tk()
f = MyFrame(root)
f.pack()
f.mainloop()

