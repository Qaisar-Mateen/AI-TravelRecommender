import customtkinter as ctk

class Card(ctk.CTkFrame):
    def __init__(self, *args, title=None, width: int = 100, height: int = 32, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)



# class Card(ctk.Frame):
#     def __init__(self, parent, title, text):
#         ctk.Frame.__init__(self, parent)
#         self.title = ctk.Label(self, text=title)
#         self.title.pack()
#         self.text = ctk.Label(self, text=text)
#         self.text.pack()

if __name__ == '__main__':
    app = ctk.CTk()
    app.title('CustomTkinter')
    app.geometry('800x600')

    card = Card(app, title='Title', width=350, height=250, corner_radius=19, fg_color='gray') #bg_color='white')
    card.place(x=800/2, y=600/2, anchor='center')


    app.mainloop()