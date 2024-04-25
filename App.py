import customtkinter as ctk
from PIL import Image
import tkinter as tk
import tkintermapview as map
from HybridRecommender import HybridRecommender
#import pandas as pd

class Card(ctk.CTkFrame):
    def __init__(self, *args, title=None, width: int = 250, height: int = 275, cr: int = 19, image=None, **kwargs):
        super().__init__(*args, corner_radius=cr, width=width, height=height, **kwargs)

        self.image_dim = (width-32, (height*0.45)-7)

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
        
        self.button_detail = ctk.CTkButton(self.body, text='View Detail', corner_radius=cr, command=lambda x: self.view_detail(title)
        self.button_detail.grid(row=1, column=3, pady=(8,13), padx=5)


    def search(self):
        self.map_widget.delete_all_marker()
        if self.search_entry.get() == '':
            return
        
        try:
            self.map_widget.set_address(self.search_entry.get(), marker=True)
            #self.map_widget.set_zoom(10)
            self.map_widget.update()

        except Exception as e:
            tk.messagebox.showerror('Error', str(e))

    def satelite_tile(self):
        if self.map_widget.tile_server != "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga")
            self.map_widget.update()

    def default_tile(self):
        if self.map_widget.tile_server != "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga":
            self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
            self.map_widget.update()

    def view_detail(self, country):
            
        top = ctk.CTkToplevel()
        top.title('Details')
        top.geometry('900x700')
        top.columnconfigure((0,6), weight=1)

        search_frame = ctk.CTkFrame(top, width=400, height=40, corner_radius=19, fg_color='transparent')
        search_frame.grid(row=0, column=1, padx=10, pady=(10,5), columnspan=3)
        search_frame.columnconfigure((0,7), weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, width=400, height=30, corner_radius=19)
        self.search_entry.grid(row=0, column=1)

        search_button = ctk.CTkButton(search_frame, text='', width=20, height=30, fg_color='#1A1A1A',
                                    corner_radius=19, command=self.search, hover_color='#373737',
                                    image=ctk.CTkImage(dark_image=Image.open('Images/search.png'),size=(15,15)))
        search_button.grid(row=0, column=2, padx=5)

        map_frame = ctk.CTkFrame(top, width=800, height=500)
        map_frame.grid(row=1, column=1, padx=10, pady=10)
        map_frame.columnconfigure((0,7), weight=1)

        self.map_widget = map.TkinterMapView(map_frame, width=750, height=450, corner_radius=19)
        self.map_widget.grid(row=0, column=1, padx=1, pady=1)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga")
       
        self.map_widget.set_address(country, marker=True)
        self.map_widget.set_zoom(8)

        sat_but = ctk.CTkButton(self.map_widget, text='', width=26, height=26, command=self.satelite_tile,
                                image=ctk.CTkImage(dark_image=Image.open('Images/satellite.png'), size=(20,20)),
                                corner_radius=2, fg_color='#333333', hover_color='#555555'
                                )
        sat_but.place(x=15, y=81, anchor='nw')

        def_but = ctk.CTkButton(self.map_widget, text='', width=26, height=26, command=self.default_tile,
                                image=ctk.CTkImage(dark_image=Image.open('Images/default.png'), size=(20,20)),
                                corner_radius=2, fg_color='#333333', hover_color='#555555'
                                )
        def_but.place(x=15, y=114, anchor='nw')


        detail = ctk.CTkFrame(top, width=800, height=200, corner_radius=19, fg_color='black')
        detail.grid(row=2, column=1, padx=10, pady=10)

        top.grab_set()
        top.mainloop()
    


if __name__ == '__main__':

    ctk.AppearanceModeTracker.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    app = ctk.CTk()
    app.title('CustomTkinter')
    app.geometry('1323x650')

    app.resizable(False, False)


    home = ctk.CTkScrollableFrame(app, width=1310, height=650, corner_radius=0, fg_color='transparent')
    home.place(x=0, y=0, anchor='nw')

    recomendation = HybridRecommender(collaborative_model=(True, 0, 'CF_Neural_Model3.7.bin'),
                    popularity_model=True,
                    popular_weight=0.2, collab_weight=0.8)
    
    rec = recomendation.recommend(top_n=16)

    cards = []

    for i in range(len(rec)):
        card = Card(home, title=rec['Country'].iloc[i], cr=19, fg_color='gray29', border_width=5)
        card.grid(row=i//4, column=i%4, padx=(40, 0), pady=(40, 0))
        cards.append(card)

    app.mainloop()