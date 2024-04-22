import customtkinter as ctk
from PIL import Image

class Card(ctk.CTkFrame):
    def __init__(self, *args, title=None, width: int = 250, height: int = 275, cr: int = 19, image=None, **kwargs):
        super().__init__(*args, corner_radius=cr, width=width, height=height, **kwargs)

        self.image_dim = (width-32, (height*0.4)-7)

        if image is None:
            self.image = ctk.CTkImage(dark_image=Image.open('no image d.png'), 
                                    light_image=Image.open('no image l.png'), 
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
        pass
    
    
if __name__ == '__main__':

    ctk.AppearanceModeTracker.set_appearance_mode('dark')
    ctk.set_default_color_theme('dark-blue')

    app = ctk.CTk()
    app.title('CustomTkinter')
    app.geometry('800x600')

    card = Card(app, title='Title', cr=19, fg_color='gray29', border_width=5)
    card.grid(row=0, column=0, padx=20, pady=20)

    ctk.CTkFrame(app, width=250, height=275, corner_radius=19).grid(row=0, column=1)
    app.mainloop()