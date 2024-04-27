import customtkinter as ctk
from PIL import Image
import tkinter as tk
import tkintermapview as map
from HybridRecommender import HybridRecommender
import pandas as pd
import requests
from requests.structures import CaseInsensitiveDict
url = '''https://api.geoapify.com/v2/places?categories=catering.restaurant,accommodation.hotel,
accommodation.hut,activity,sport,heritage,ski,tourism,leisure,natural,rental.bicycle,rental.ski,entertainment
&conditions=named,access.yes&filter=geometry:9bf70c418b06f172dbd53d509b13b913&bias=proximity:74.3271803,31.5826618
&limit=20&apiKey=d76f029b27e04a9cb47a5356a7bf2a87'''


# res = requests.get(url)
# print(res.json())


special_cases = {'Greenland': 'Kalaallit Nunaat', 'Bangladesh': 'Dhaka,Bangladesh', 'Jordan': 'Amman,Jordan', 'Lebanon': 'Beirut,Lebanon',
                'palau': 'Ngerulmud,palau', 'Armenia': 'Yerevan,Armenia', 'Sudan':'Khartoum,Sudan'}

def get_spots(country):
    df = pd.read_csv('world-cities.csv')

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
        
        self.button_detail = ctk.CTkButton(self.body, text='View Detail', corner_radius=cr, command=lambda: self.view_detail(title))
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
        global special_cases

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
        

        a = self.map_widget.set_address(special_cases.get(country)if special_cases.get(country)else country,marker=True,text=country)
        if a == False:
            tk.messagebox.showerror('Error', str('Address Not Found!!'))

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
    
def load_more(cur, cards, btn_fr, home):
    
    btn_fr.grid_forget()
    total = cur + 12
    if total > 222:
        total = 222
    
    rec = recomendation.recommend(top_n=total)
    for i in range(cur, total):
        card = Card(home, title=rec['Country'].iloc[i], cr=19, fg_color='gray29', border_width=5)
        card.grid(row=1+i//4, column=i%4, padx=(40, 0), pady=(40, 0))
        cards.append(card)
    
    if total < 222:
        btn_fr.grid(row=2+len(cards)//4, column=0, columnspan=4, pady=30, sticky='ew')
    else:
        ctk.CTkLabel(home, text='', fg_color='transparent').grid(row=2+len(cards)//4, column=0, columnspan=4, pady=20)

def login():
    global id

    master = tk.Tk()
    master.title('Login')
    master.geometry('1323x650')
    fr = ctk.CTkFrame(master, width=400, height=200, corner_radius=19)
    fr.place(x=1323//2, y=650/2, anchor='center')
    fr.columnconfigure((0,7), weight=1)

    def login_action(user_id, fr):
        global id
        try:
            user_id = int(user_id)
            ids = pd.read_csv('ratings.csv')
            ids = ids['user'].unique()
            if user_id in ids:
                fr.destroy()
                id = user_id
            else:
                raise ValueError('User ID not found!!')
        except ValueError as e:
            tk.messagebox.showerror('Error', str(e))
        except Exception as e:
            tk.messagebox.showerror('Error', 'An unexpected error occurred: ' + str(e))


    ctk.CTkLabel(fr, text='Login', font=('Arial', 20, 'bold')).grid(row=0, column=1, pady=(10, 20))

    ent = ctk.CTkEntry(fr, placeholder_text='Enter User ID', height=30, corner_radius=19)
    ent.grid(row=1, column=1, pady=10, padx=10)
    btn = ctk.CTkButton(fr, text='Login', corner_radius=19, height=30, width=90, command=lambda: login_action(ent.get(), master))
    btn.grid(row=2, column=1, pady=10, padx=10)
    
    master.mainloop()

if __name__ == '__main__':
    global id
    
    id = input('LoginID: ')#login()
    print(id)
    if id != -1 or id is not None:
        ctk.AppearanceModeTracker.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        app = ctk.CTk()
        app.title('AI-Travel Recommender')
        app.geometry('1323x650')
        app.resizable(False, False)

        home = ctk.CTkScrollableFrame(app, width=1310, height=650, corner_radius=0, fg_color='transparent')
        home.place(x=0, y=0, anchor='nw')
        ctk.CTkLabel(home, text='Top Destinations for you', font=('Arial', 20, 'bold')).grid(row=0, column=0, pady=(30,2))
    
        recomendation = HybridRecommender(collaborative_model=(True, id, 'CF_Neural_Model3.7.bin'),
                    popularity_model=True,
                    popular_weight=0.2, collab_weight=0.8
                    )
        rec = recomendation.recommend(top_n=16)

        cards = []
        for i in range(len(rec)):
            card = Card(home, title=rec['Country'].iloc[i], cr=19, fg_color='gray29', border_width=5)
            card.grid(row=1+i//4, column=i%4, padx=(40, 0), pady=(40, 0))
            cards.append(card)
    
        btn_fr = ctk.CTkFrame(home, fg_color='transparent')
        btn_fr.grid(row=2+len(cards)//4, column=0, columnspan=4, pady=30, sticky='ew')
        btn_fr.columnconfigure((0,3), weight=1)

        btn = ctk.CTkButton(btn_fr, text='Load More', font=('Arial', 12), corner_radius=19, fg_color='#1A1A1A', height=30,
                        hover_color='#373737', command=lambda: load_more(len(cards), cards, btn_fr, home), width=100
                        )
        btn.grid(row=0, column=2, padx=10, pady=1)
        ctk.CTkFrame(btn_fr, fg_color='transparent', width=35, height=30).grid(row=0, column=1)

    app.mainloop()