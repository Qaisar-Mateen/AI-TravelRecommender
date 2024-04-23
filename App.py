import customtkinter as ctk
from PIL import Image
import tkinter as tk
import tkintermapview as map

class Card(ctk.CTkFrame):
    def __init__(self, *args, title=None, width: int = 250, height: int = 275, cr: int = 19, image=None, **kwargs):
        super().__init__(*args, corner_radius=cr, width=width, height=height, **kwargs)

        self.image_dim = (width-32, (height*0.4)-7)

        if image is None:
            self.image = ctk.CTkImage(dark_image=Image.open('Images/no image d.png'), 
                                    light_image=Image.open('Images/no image l.png'), 
                                    size=self.image_dim)
            self.image_label = ctk.CTkLabel(self, image=self.image, text='', corner_radius=cr)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=16, pady=(5, 2), sticky="ewn")
        
        else:
            self.image = ctk.CTkImage(dark_image=Image.open('Images/' + image), 
                                    light_image=Image.open('Images/' + image), 
                                    size=self.image_dim)
            self.image_label = ctk.CTkLabel(self, image=self.image, text='', corner_radius=cr)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=16, pady=(5, 2), sticky="ewn")
        
        self.body_dim = (width-16, height*0.6)
        self.body = ctk.CTkFrame(self, width=self.body_dim[0], height=self.body_dim[1], corner_radius=cr, border_width=3)
        self.body.grid(row=1, column=0, columnspan=3, pady=(5, 8), padx=8, sticky="ews")

        self.body.grid_columnconfigure((0,7), weight=1)

        self.title = ctk.CTkLabel(self.body, text=title, corner_radius=cr, font=('Arial', 14, 'bold'))
        self.title.grid(row=0, column=3, pady=5, padx=5)
        
        self.button_detail = ctk.CTkButton(self.body, text='View Detail', corner_radius=cr, command=self.view_detail)
        self.button_detail.grid(row=1, column=3, pady=8, padx=5)

    def view_detail(self):
            # create map widget
        top = ctk.CTkToplevel()
        top.title('Details')
        top.geometry('800x600')
        
        map_widget = map.TkinterMapView(top, width=800, height=600, corner_radius=0)
        map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        top.grab_set()
        top.mainloop()
    

home = None

if __name__ == '__main__':

    ctk.AppearanceModeTracker.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    app = ctk.CTk()
    app.title('CustomTkinter')
    app.geometry('1323x650')

    x = 0
    y = 0

    home = ctk.CTkScrollableFrame(app, width=1310, height=650, corner_radius=0, fg_color='transparent')
    home.place(x=x, y=y, anchor='nw')


    def move():
        global home, x, y
        if home is None:
            return
        
        x = x+70
        home.place_configure(x=x, y=y, anchor='nw')
        if x < 1900 and y < 800:
            app.after(1, move)
    
   
    card = Card(home, title='Title1', cr=19, fg_color='gray29', border_width=5)
    card.grid(row=0, column=0, padx=(40, 0), pady=(40, 0))
    
    card2 = Card(home, title='Title2', cr=19, fg_color='gray29', border_width=5)
    card2.grid(row=0, column=1, padx=(40, 0), pady=(40, 0))

    card3 = Card(home, title='Title3', cr=19, fg_color='gray29', border_width=5)
    card3.grid(row=0, column=2, padx=(40, 0), pady=(40, 0))
    
    card4 = Card(home, title='Title4', cr=19, fg_color='gray29', border_width=5)
    card4.grid(row=0, column=3, padx=(40, 0), pady=(40, 0))


    card5 = Card(home, title='Title5', cr=19, fg_color='gray29', border_width=5)
    card5.grid(row=1, column=0, padx=(40, 0), pady=(40, 0))
    
    card6 = Card(home, title='Title6', cr=19, fg_color='gray29', border_width=5)
    card6.grid(row=1, column=1, padx=(40, 0), pady=(40, 0))

    card7 = Card(home, title='Title7', cr=19, fg_color='gray29', border_width=5)
    card7.grid(row=1, column=2, padx=(40, 0), pady=(40, 0))
    
    card8 = Card(home, title='Title8', cr=19, fg_color='gray29', border_width=5)
    card8.grid(row=1, column=3, padx=(40, 0), pady=(40, 0))

    move()

    app.mainloop()