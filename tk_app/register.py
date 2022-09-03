import tkinter as tk
from tkinter import  ttk
from PIL import Image, ImageTk
import time
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

def transform_num(frame,x):
    try:
        x = int(x)
        return x
    except ValueError:
        try:
            x = float(x)
            return int(x)
        except ValueError:
            return frame.error_reg_label.grid(row=5,column=0,sticky='e',pady=20), frame.success_reg_label.grid_forget()

def register_product(frame):
    
    try:
        d = {
            "product_name": frame.product_name.get(),
            "merchant": frame.merchant.get(),
            "mark": frame.mark.get(),
            "cost": transform_num(frame,frame.cost.get()),
            "price": transform_num(frame,frame.price.get()),
            "stock": transform_num(frame,frame.stock.get())
        }
        for x in d:
            if d[x] == '':
                return frame.error_reg_label.grid(row=5,column=0,sticky='e',pady=20), frame.success_reg_label.grid_forget()

        try:
            cursor.execute("INSERT INTO productos (producto,proveedor,marca,costo,precio,stock) values (?,?,?,?,?,?)", (
                d["product_name"],
                d["merchant"],
                d["mark"],
                d["cost"],
                d["price"],
                d["stock"])
            )
            conn.commit()
            frame.product_name.delete(0,tk.END)
            frame.merchant.delete(0,tk.END)
            frame.mark.delete(0,tk.END)
            frame.cost.delete(0,tk.END)
            frame.price.delete(0,tk.END)
            frame.stock.delete(0,tk.END)
            return frame.success_reg_label.grid(row=5,column=0,sticky='e',pady=20),frame.error_reg_label.grid_forget()
            
        except:
            cursor.execute("CREATE TABLE productos (id INTEGER PRIMARY KEY, Producto TEXT,Proveedor TEXT,Marca TEXT,Costo INTEGER,Precio INTEGER,Stock INTEGER)")

            
            cursor.execute("INSERT INTO productos (producto,proveedor,marca,costo,precio,stock) values (?,?,?,?,?,?)", (
                    d["product_name"],
                    d["merchant"],
                    d["mark"],
                    d["cost"],
                    d["price"],
                    d["stock"]
                )
            ) 
            conn.commit()
            frame.product_name.delete(0,tk.END)
            frame.merchant.delete(0,tk.END)
            frame.mark.delete(0,tk.END)
            frame.cost.delete(0,tk.END)
            frame.price.delete(0,tk.END)
            frame.stock.delete(0,tk.END)
            return frame.success_reg_label.grid(row=5,column=0,sticky='e',pady=20),frame.error_reg_label.grid_forget()

    except:
        return frame.error_reg_label.grid(row=5,column=0,sticky='e',pady=20),frame.success_reg_label.grid_forget()

def register_offer(frame):
    try:
        identifiers = []
        i_text = ""
        compounds = [
            {"select": frame.select_one.get(), "stock": frame.one_stock.get()},
            {"select": frame.select_two.get(), "stock": frame.two_stock.get()},
            {"select": frame.select_three.get(), "stock": frame.three_stock.get()},
            {"select": frame.select_four.get(), "stock": frame.four_stock.get()},
            {"select": frame.select_five.get(), "stock": frame.five_stock.get()}
        ]

        for c in compounds:
            if c["select"] == '' or c["stock"] == '':
                continue
            else:
                if c["stock"].isdecimal() == True:
                    identifiers.append((c["select"].split(" - ")[0],c["stock"]))
                    
                else:
                   return frame.error_label.grid(row=15,column=0,sticky='e',padx=20,pady=40), frame.success_label.grid_forget()
        try:
            for x in identifiers:
                i_text += f"{x[0]},{x[1]};"
            if frame.offer_name.get() == '' or frame.offer_price.get().isdecimal() == False:
                return frame.error_label.grid(row=15,column=0,sticky='e',padx=20,pady=40), frame.success_label.grid_forget()
            else:
                cursor.execute("INSERT INTO promociones (promocion, identificadores, precio) values (?,?,?)", (frame.offer_name.get(), i_text, int(frame.offer_price.get())))
                conn.commit()
                return frame.success_label.grid(row=15,column=0,sticky='e',padx=20,pady=40), frame.error_label.grid_forget()
        except sqlite3.OperationalError:
            cursor.execute("CREATE TABLE promociones (id INTEGER PRIMARY KEY, promocion TEXT, identificadores TEXT, precio INTEGER)")
            cursor.execute("INSERT INTO promociones (promocion, identificadores, precio) values (?,?,?)", (frame.offer_name.get(), str((i+";" for i in identifiers)), frame.offer_price.get()))
            conn.commit()
            return frame.success_label.grid(row=15,column=0,sticky='e',padx=20,pady=40), frame.error_label.grid_forget()
    except:
        return frame.error_label.grid(row=15,column=0,sticky='e',padx=20,pady=40), frame.success_label.grid_forget()



####################### APP PRINCIPAL ###########################

class Window(tk.Tk):
    def __init__(self, *args):
        super().__init__(*args)

        self.title("Registro de mercancía")
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)

        main_container = tk.Frame(self)
        main_container.grid(sticky='nsew')

        self.all_frames = {}

        for x in (AddProduct, Offers, Edit, Delete, Prices, Statistics, Sales):
            frame = x(self, main_container)
            self.all_frames[x] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        
        self.show(AddProduct)

    def show(self, required_frame):
        frame = self.all_frames[required_frame]

        frame.tkraise()

################### NUEVO PRODUCTO ######################

class AddProduct(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        new_merch = tk.Label(self, text="INGRESO DE PRODUCTOS",font='bold',pady=30)
        new_merch.grid(row=0,column=1,sticky='nsew')

        product_name_label = tk.Label(self, text="Nombre del producto",justify='left')
        product_name_label.grid(row=1,column=0,padx=20,pady=10,sticky='sw')
        self.product_name = ttk.Entry(self, width=40)
        self.product_name.grid(row=2,column=0,padx=20,sticky='w')

        merchant_label = tk.Label(self, text="Proveedor",justify='left')
        merchant_label.grid(row=1,column=1,pady=10,sticky='sw',padx=20)
        self.merchant = ttk.Entry(self, width=40)
        self.merchant.grid(row=2,column=1,padx=20,sticky='w')

        mark_label = tk.Label(self, text="Marca",justify='left')
        mark_label.grid(row=1,column=2,pady=10,sticky='sw',padx=20)
        self.mark = ttk.Entry(self, width=20)
        self.mark.grid(row=2,column=2,padx=20,sticky='w')

        cost_label = tk.Label(self, text="Costo",justify='left')
        cost_label.grid(row=3,column=0,pady=10,sticky='sw',padx=20)
        self.cost = ttk.Entry(self, width=20)
        self.cost.grid(row=4,column=0,padx=20,sticky='w')

        price_label = tk.Label(self, text="Precio de venta",justify='left')
        price_label.grid(row=3,column=1,pady=10,sticky='sw',padx=20)
        self.price = ttk.Entry(self, width=20)
        self.price.grid(row=4,column=1,padx=20,sticky='w')

        stock_label = tk.Label(self, text="Stock",justify='left')
        stock_label.grid(row=3,column=2,pady=10,sticky='sw',padx=20)
        self.stock = ttk.Entry(self, width=10)
        self.stock.grid(row=4,column=2,padx=20,sticky='w')

        self.error_reg_label = tk.Label(self, text="Uno de los campos es inválido",fg='red')
        self.success_reg_label = tk.Label(self, text=f"¡Añadido con éxito!",fg='green')

        reg_button = tk.Button(self, text="Ingresar",command=lambda:register_product(self))
        reg_button.grid(row=5,column=1,pady=20,padx=40,sticky='e')

################### OFERTAS ###################

class Offers(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        cursor.execute("select id, producto, stock from productos")

        create_offer_label = tk.Label(self, text="INGRESAR PROMOCIONES", font='bold', pady=30)
        create_offer_label.grid(row=0,column=1,sticky='n')

        offer_name_label = tk.Label(self,text="NOMBRE DE LA PROMOCIÓN")
        offer_name_label.grid(row=1,column=0,sticky='w',padx=20,pady=10)
        self.offer_name = ttk.Entry(self,width=40)
        self.offer_name.grid(row=2,column=0,sticky='w',padx=20)

        select_one_label = tk.Label(self, text="Seleccionar producto")
        select_one_label.grid(row=3,column=0,sticky='w',padx=20,pady=10)
        self.select_one = ttk.Combobox(self, width=50, postcommand=self.update_boxes)
        self.select_one.grid(row=4,column=0,sticky='w',padx=20)
        one_stock_label = tk.Label(self, text="Cantidad")
        one_stock_label.grid(row=3, column=1, sticky='w',padx=20)
        self.one_stock = ttk.Entry(self, width=10)
        self.one_stock.grid(row=4,column=1,sticky='w',padx=20)

        select_two_label = tk.Label(self, text="Seleccionar producto")
        select_two_label.grid(row=5,column=0,sticky='w',padx=20,pady=10)
        self.select_two = ttk.Combobox(self, width=50, postcommand=self.update_boxes)
        self.select_two.grid(row=6,column=0,sticky='w',padx=20)
        two_stock_label = tk.Label(self, text="Cantidad")
        two_stock_label.grid(row=5,column=1,sticky='w',padx=20,pady=10)
        self.two_stock = ttk.Entry(self,width=10)
        self.two_stock.grid(row=6, column=1, sticky='w',padx=20)

        select_three_label = tk.Label(self, text="Seleccionar producto")
        select_three_label.grid(row=7,column=0,sticky='w',padx=20,pady=10)
        self.select_three = ttk.Combobox(self, width=50, postcommand=self.update_boxes)
        self.select_three.grid(row=8,column=0,sticky='w',padx=20)
        three_stock_label = tk.Label(self, text="Cantidad")
        three_stock_label.grid(row=7,column=1,sticky='w',padx=20,pady=10)
        self.three_stock = ttk.Entry(self, width=10)
        self.three_stock.grid(row=8,column=1,sticky='w',padx=20)

        select_four_label = tk.Label(self, text="Seleccionar producto")
        select_four_label.grid(row=9,column=0,sticky='w',padx=20,pady=10)
        self.select_four = ttk.Combobox(self,width=50, postcommand=self.update_boxes)
        self.select_four.grid(row=10,column=0,sticky='w',padx=20)
        four_stock_label = tk.Label(self,text="Cantidad")
        four_stock_label.grid(row=9,column=1,sticky='w',padx=20,pady=10)
        self.four_stock = ttk.Entry(self,width=10)
        self.four_stock.grid(row=10,column=1,sticky='w',padx=20)

        select_five_label = tk.Label(self, text="Seleccionar producto")
        select_five_label.grid(row=11,column=0,sticky='w',padx=20,pady=10)
        self.select_five = ttk.Combobox(self, width=50, postcommand=self.update_boxes)
        self.select_five.grid(row=12,column=0,sticky='w',padx=20)
        five_stock_label = tk.Label(self,text="Cantidad")
        five_stock_label.grid(row=11,column=1,sticky='w',padx=20,pady=10)
        self.five_stock = ttk.Entry(self,width=10)
        self.five_stock.grid(row=12,column=1,sticky='w',padx=20)

        offer_price_label = tk.Label(self, text="Precio")
        offer_price_label.grid(row=13,column=1,sticky='w',padx=20,pady=10)
        self.offer_price = ttk.Entry(self,width=10)
        self.offer_price.grid(row=14,column=1,sticky='w',padx=20)

        self.error_label = tk.Label(self, text="Uno de los campos es inválido",fg='red')
        self.success_label = tk.Label(self, text="¡Promoción añadida con éxito!",fg='green')

        offer_button = tk.Button(self,text="Registrar",command=lambda:register_offer(self))
        offer_button.grid(row=15,column=1,sticky='e',pady=40)

    def update_boxes(self):
        cursor.execute('select id,producto,stock from productos')
        all_products = [f"{i} - {product} ({stock} disponibles)" for i, product, stock in cursor.fetchall()]
        self.select_one['values'] = all_products
        self.select_two['values'] = all_products
        self.select_three['values'] = all_products
        self.select_four['values'] = all_products
        self.select_five['values'] = all_products

######################## EDITAR PRODUCTOS ##########################

class Edit(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        update_label = tk.Label(self,text="ACTUALIZAR PRODUCTOS",font='bold',pady=30)
        update_label.grid(row=0,column=0,sticky='e')

        select_label = tk.Label(self, text="Seleccione el producto")
        select_label.grid(row=1,column=0,sticky='w',padx=20,pady=10)
        self.update_p = ttk.Combobox(self, width=70, postcommand=self.update_box)
        self.update_p.grid(row=2,column=0,padx=20)

        price_label = tk.Label(self, text="Nuevo precio")
        price_label.grid(row=3,column=0,sticky='w',padx=20,pady=10)
        self.price = ttk.Entry(self,width=15)
        self.price.grid(row=4,column=0,sticky='w',padx=20)

        stock_label = tk.Label(self,text="Añadir stock")
        stock_label.grid(row=5,column=0,sticky='w',padx=20,pady=10)
        self.stock = ttk.Entry(self,width=15)
        self.stock.grid(row=6,column=0,sticky='w',padx=20)

        update_button = tk.Button(self,text="Actualizar",command=self.update_product)
        update_button.grid(row=7,column=1,sticky='e',padx=20,pady=30)

        self.error_label = tk.Label(self,text="Uno de los campos es inválido",fg='red')
        self.success_label = tk.Label(self, text="Producto actualizado",fg='green')

    def update_box(self):
        cursor.execute("select id, producto, proveedor, precio, stock from productos")
        all_products = [f"{i} - {product} | {merchant} | {price}$ ({stock} disponibles)" for i, product, merchant, price, stock in cursor.fetchall()]
        self.update_p['values'] = all_products

    def update_product(self):
        try:
            product = self.update_p.get().split(" - ")[0]
            cursor.execute(f"select stock from productos where id = {product}")
            current_stock = cursor.fetchall()[0][0]
            if self.stock.get() != '' and self.price.get() != '':
                added_stock = str(int(self.stock.get())+int(current_stock))
                cursor.execute(f"UPDATE productos SET stock = {added_stock}, precio = {self.price.get()} where id = {product}")
                conn.commit()
            elif self.stock.get() == '' and self.price.get() != '':
                cursor.execute(f"UPDATE productos SET precio = {self.price.get()} where id = {product}")
                conn.commit()
            else:
                added_stock = str(int(self.stock.get())+int(current_stock))
                cursor.execute(f"UPDATE productos set stock = {added_stock} where id = {product}")
                conn.commit()
            return self.success_label.grid(row=7,column=0,sticky='w',padx=20,pady=10),self.error_label.grid_forget()
        except:
            return self.error_label.grid(row=7,column=0,sticky='w',padx=20,pady=10),self.success_label.grid_forget()


######################## BORRAR PRODUCTOS ###########################

class Delete(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        delete_label = tk.Label(self,text="ELIMINAR PRODUCTOS",font='bold',pady=30)
        delete_label.grid(row=0,column=1,sticky='nsew')

        choose_label = tk.Label(self, text="Seleccione el producto")
        choose_label.grid(row=1,column=0,sticky='w',padx=20,pady=10)
        self.choose = ttk.Combobox(self,width=50,postcommand=self.update_box)
        self.choose.grid(row=2,column=0,sticky='w',padx=20)

        self.success_label = tk.Label(self, fg='green')
        self.error_label = tk.Label(self, text="Uno de los campos es inválido", fg='red')

        delete_button = tk.Button(self,text="Eliminar",command=self.delete_product)
        delete_button.grid(row=2,column=1,sticky='w',padx=20)

        choose_offer_label = tk.Label(self, text="Seleccione la promoción")
        choose_offer_label.grid(row=3,column=0,sticky='w',padx=20,pady=10)
        self.choose_offer = ttk.Combobox(self,width=50,postcommand=self.update_offers)
        self.choose_offer.grid(row=4,column=0,sticky='w',padx=20)

        delete_offer_button = tk.Button(self, text="Eliminar", command=self.delete_offer)
        delete_offer_button.grid(row=4,column=1, sticky='w',padx=20)

    def update_box(self):
        cursor.execute("select id,producto,stock from productos")
        all_products = [f"{i} - {producto} ({stock} disponibles)" for i, producto, stock in cursor.fetchall()]
        self.choose['values'] = all_products

    def update_offers(self):
        cursor.execute("select id,promocion from promociones")
        all_offers = [f"{i} - {promocion}" for i, promocion in cursor.fetchall()]
        self.choose_offer['values'] = all_offers

    def delete_product(self):
        product = self.choose.get().split(" - ")[0]
        if product == '':
            return self.error_label.grid(row=5,column=0,sticky='w',padx=20,pady=10),self.success_label.grid_forget()
        else:
            offers_involved = {}
            cursor.execute("select identificadores from promociones")
            save_identifiers = cursor.fetchall()
            for x in save_identifiers:
                offers_involved[x[0]] = 0
                id_qu = x[0].split(";")
                del(id_qu[-1])
                for y in id_qu:
                    identifiers = y.split(",")[0]
                    if product == identifiers[0]:
                        offers_involved[x[0]] = 1
            for z in offers_involved:
                if offers_involved[z] == 1:
                    cursor.execute(f"DELETE FROM promociones where identificadores = '{z}'")
                    conn.commit()
            cursor.execute(f"DELETE FROM productos where id = '{product}'")
            conn.commit()
            self.success_label['text'] = f"Producto {product} eliminado"
            self.choose.delete(0,tk.END)
            return self.success_label.grid(row=5,column=0,sticky='w',padx=20,pady=10),self.error_label.grid_forget()

    def delete_offer(self):
        product = self.choose_offer.get().split(" - ")[0]
        cursor.execute(f"DELETE FROM promociones where id = {product}")
        conn.commit()
        self.success_label['text'] = f"Promoción {product} eliminada"
        self.choose_offer.delete(0,tk.END)
        return self.success_label.grid(row=5,column=0,sticky='w',padx=20,pady=10)

######################## CONTROL DE PRECIOS #########################

class Prices(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        label = tk.Label(self,text="ACTUALIZAR PRECIOS",font='bold',padx=30)
        label.grid(row=0,column=0,sticky='nsew',pady=30)

        select_label = tk.Label(self, text="Seleccione el producto")
        select_label.grid(row=1,column=0,sticky='w',padx=20,pady=10)
        self.update_p = ttk.Combobox(self, width=70, postcommand=self.update_box)
        self.update_p.grid(row=2,column=0,padx=20)

        new_price_label = tk.Label(self, text="Ingrese el porcentaje de aumento")
        new_price_label.grid(row=3,column=0,sticky='w',padx=20,pady=10)
        self.new_price = ttk.Entry(self,width=3)
        self.new_price.grid(row=3,column=1,sticky='w',pady=10)
        percent_label = tk.Label(self,text="%")
        percent_label.grid(row=3,column=2,sticky='w',pady=10)

        new_price_button = tk.Button(self, text="Actualizar",command=self.update_product_percent)
        new_price_button.grid(row=3,column=3,sticky='w',padx=20,pady=10)

        self.error_label = tk.Label(self,text="Uno de los campos es inválido",fg='red')
        self.success_label = tk.Label(self,text="Precio actualizado",fg='green')

    def update_box(self):
        cursor.execute("select id, producto, proveedor, precio, stock from productos")
        all_products = [f"{i} - {product} | {merchant} | {price}$ ({stock} disponibles)" for i, product, merchant, price, stock in cursor.fetchall()]
        self.update_p['values'] = all_products

    def update_product_percent(self):
        try:
            product = self.update_p.get().split(" - ")[0]
            cursor.execute(f"select precio from productos where id = {product}")
            price = cursor.fetchall()[0][0]
            percent = self.new_price.get()
            if len(percent) == 1:
                factor = float(f"1.0{percent}")
            elif len(percent) == 2:
                factor = float(f"1.{percent}")
            else:
                return self.error_label.grid(row=4,column=0,sticky='w',padx=20,pady=10),self.success_label.grid_forget()
            new_price = price*factor
            cursor.execute(f"UPDATE productos SET precio = {str(new_price)} where id = {product}")
            conn.commit()
            return self.success_label.grid(row=4,column=0,sticky='w',padx=20,pady=10),self.error_label.grid_forget()
        except:
            return self.error_label.grid(row=4,column=0,sticky='w',padx=20,pady=10),self.success_label.grid_forget() 

######################## ESTADÍSTICAS GENERALES ######################

class Statistics(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        statistics_label = tk.Label(self, text="ESTADÍSTICAS DEL MES",font='bold',pady=30)
        statistics_label.grid(row=0,column=0,sticky='nsew')

        # update_button = tk.Button(self, text="Actualizar", command=self.create_img)
        # update_button.grid(row=1,column=0,sticky='nsew')

        current_month = time.asctime()
        current_month = current_month[4:7]+current_month.split()[-1]

        products = [x[0] for x in cursor.execute("select producto from productos order by id").fetchall()]
        positions = np.arange(len(products))
        sales = np.array([x[0] for x in cursor.execute(f"select {current_month} from productos order by id").fetchall()])
        
        fig, ax = plt.subplots()
        fig.subplots_adjust(left=0.22)
        ax.barh(positions,sales,align='center')
        ax.set_yticks(positions,labels=products,fontsize=8)
        
        ax.set_xlabel("Ventas")
        fig.suptitle("Cantidad de productos vendidos")


        img = plt.savefig("current.jpg")
        open = Image.open("current.jpg")
        ph = ImageTk.PhotoImage(open)
        img_label = tk.Label(self, image=ph)
        img_label.image=ph
        img_label.grid(row=2,column=0,sticky='nsew',padx=20,pady=20)

        

######################## REGISTRO DE VENTAS ###########################

class Sales(tk.Frame):
    def __init__(self, container, control, *args):
        super().__init__(container, *args)

        sales_label = tk.Label(self, text="VENTAS",font='bold',pady=30)
        sales_label.grid(row=0,column=1,sticky='nsew')

        choose_label = tk.Label(self, text="Seleccione el producto")
        choose_label.grid(row=1,column=0,sticky='w',padx=20,pady=10)
        cursor.execute("select id, producto, stock from productos")
        self.choose = ttk.Combobox(self, width=50, postcommand=self.update_box)
        self.choose.grid(row=2,column=0,sticky='w',padx=20,pady=0)

        quantity_label = tk.Label(self, text="Cantidad")
        quantity_label.grid(row=1,column=1,sticky='w',padx=20,pady=10)
        self.quantity = ttk.Entry(self,width=10)
        self.quantity.grid(row=2, column=1, sticky='w',padx=20)

        sale_button = tk.Button(self, text="Añadir", command=self.add_product_to_bill)
        sale_button.grid(row=2,column=2, sticky='e', pady=20)

        choose_offers_label = tk.Label(self, text="Seleccione la promoción")
        choose_offers_label.grid(row=4, column=0,sticky='w',padx=20,pady=10)
        self.choose_offers = ttk.Combobox(self, width=50, postcommand=self.update_offers)
        self.choose_offers.grid(row=5,column=0, sticky='w',padx=20)

        offers_quantity_label = tk.Label(self, text="Cantidad")
        offers_quantity_label.grid(row=4,column=1,sticky='w',padx=20,pady=10)
        self.offers_quantity = ttk.Entry(self,width=10)
        self.offers_quantity.grid(row=5,column=1,sticky='w',padx=20)

        self.error_label = tk.Label(self, text="Uno de los campos es inválido",fg='red')
        self.no_stock_label = tk.Label(self, text="Pedido cancelado",fg='red')
        self.neg_stock_label = tk.Label(self, text="Stock insuficiente", fg='red')
        self.sent_label = tk.Label(self, text="Venta registrada",fg='green')

        offer_button = tk.Button(self, text="Añadir",command=self.add_offer_to_bill)
        offer_button.grid(row=5, column=2,sticky='e',pady=20)

        cancel_button = tk.Button(self, text="Cancelar",command=self.delete_bill)
        cancel_button.grid(row=6,column=1,sticky='e',padx=20,pady=20)

        send_button = tk.Button(self,text="Enviar",command=self.send_sale)
        send_button.grid(row=6,column=2,sticky='w',pady=20)

        self.bill_info = ""
        self.bill_label = tk.Label(self,text=self.bill_info,fg='green')
 
        self.products_backup = {}
        self.products_before_sending = {}
        self.total = 0
        self.total_label = tk.Label(self, text=str(self.total),fg='green',font='bold')

    def delete_bill(self):
        for x in self.products_backup:
            cursor.execute(f"UPDATE productos SET stock = {self.products_backup[x]} where id = {x}")
            conn.commit()
        self.products_backup = {}
        self.products_before_sending = {}
        self.bill_info = ""
        self.bill_label['text'] = self.bill_info
        self.total = 0
        self.total_label['text'] = ""
        return self.no_stock_label.grid(row=6,column=0,sticky='w',padx=20,pady=20),self.bill_label.grid_forget(),self.error_label.grid_forget(), self.sent_label.grid_forget(),self.total_label.grid_forget(),self.neg_stock_label.grid_forget()


    def add_product_to_bill(self):
        try:
            product = self.choose.get().split(" - ")[0]
            cursor.execute(f"select stock, precio from productos where id = {product}")
            for x in cursor.fetchall():
                av = x[0]
                self.total += x[1] * int(self.quantity.get())
            rq = int(self.quantity.get())
            if av >= rq:
                result = av - rq
                cursor.execute(f"UPDATE productos SET stock = {result} WHERE id = {product};")
                conn.commit()
            if product not in self.products_backup:
                self.products_backup[product] = av
            
            self.bill_info += f"Producto {product} añadido ({rq} unidades)\n"
            self.bill_label['text'] = self.bill_info
            self.total_label['text'] = f"Precio final: {str(self.total)}$"
            try:
                self.products_before_sending[product] += rq
            except KeyError:
                self.products_before_sending[product] = rq
        
            return self.bill_label.grid(row=6,column=0,sticky='w',padx=20,pady=20), self.total_label.grid(row=7,column=0,sticky='e',padx=20,pady=20), self.error_label.grid_forget(), self.no_stock_label.grid_forget(), self.sent_label.grid_forget(),self.neg_stock_label.grid_forget()
        except:
            return self.error_label.grid(row=6, column=0, sticky='w', padx=20, pady=20), self.total_label.grid_forget(), self.no_stock_label.grid_forget(), self.sent_label.grid_forget(),self.neg_stock_label.grid_forget()

    def add_offer_to_bill(self):
        try:
            offer = self.choose_offers.get().split(" - ")[0]
            cursor.execute(f"select identificadores, precio from promociones where id = {offer}")
            for x in cursor.fetchall():
                i = x[0]
                price = x[1]
                self.total += price
            list_i = i.split(";")
            del(list_i[-1])
            for y in list_i:
                id_product = y.split(',')[0]
                stock_less = int(y.split(',')[1])
                cursor.execute(f"select stock from productos where id = {id_product}")
                try:
                    current_stock = cursor.fetchall()[0][0]
                    new_stock = current_stock - (stock_less * int(self.offers_quantity.get()))
                    cursor.execute(f"UPDATE productos SET stock = {new_stock} WHERE id = {id_product}")
                    conn.commit()
                    cursor.execute(f"select stock from productos where id = {id_product}")
                    try_stock = cursor.fetchall()[0][0]
                    if try_stock < 0:
                        cursor.execute(f"UPDATE productos SET stock = {current_stock} where id = {id_product}")
                        conn.commit()
                        self.bill_info += f"###STOCK INSUFICIENTE (promoción {offer})###\n"
                        self.bill_label['text'] = self.bill_info
                        self.total -= price
                    else:
                        self.bill_info += f"Producto {id_product} añadido ({stock_less * int(self.offers_quantity.get())} unidades)\n"
                        self.bill_label['text'] = self.bill_info

                        try:
                            self.products_before_sending[id_product] += stock_less
                        except KeyError:
                            self.products_before_sending[id_product] = stock_less

                        try:
                            if current_stock > self.products_backup[id_product]:
                                self.products_backup[id_product] = current_stock
                        except KeyError:
                            self.products_backup[id_product] = current_stock
                        self.total_label['text'] = f"Precio final: {str(self.total)}$"
                except IndexError:
                    self.total -= price
                    return self.neg_stock_label.grid(row=6,column=0,sticky='w',padx=20,pady=20),self.bill_label.grid_forget(), self.total_label.grid(row=7,column=0,sticky='e',padx=20,pady=20), self.error_label.grid_forget(), self.no_stock_label.grid_forget(), self.sent_label.grid_forget()
            return self.bill_label.grid(row=6,column=0,sticky='w',padx=20,pady=20), self.total_label.grid(row=7,column=0,sticky='e',padx=20,pady=20), self.error_label.grid_forget(), self.no_stock_label.grid_forget(), self.sent_label.grid_forget(),self.neg_stock_label.grid_forget()
        except:
            return self.error_label.grid(row=6,column=0,sticky='w',padx=20,pady=20),self.total_label.grid_forget(), self.bill_label.grid_forget(), self.no_stock_label.grid_forget(), self.sent_label.grid_forget(),self.neg_stock_label.grid_forget()

    def update_box(self):
        cursor.execute("select id,producto,stock from productos")
        all_products = [f"{i} - {producto} ({stock} disponibles)" for i, producto, stock in cursor.fetchall()]
        self.choose['values'] = all_products

    def update_offers(self):
        cursor.execute("select id,promocion from promociones")
        all_offers = [f"{i} - {promocion}" for i, promocion in cursor.fetchall()]
        self.choose_offers['values'] = all_offers

    def send_sale(self):
        self.total = 0
        self.total_label['text'] = ""
        self.bill_info = ""
        self.bill_label['text'] = self.bill_info
        current_month = time.asctime()
        current_month = current_month[4:7]+current_month.split()[-1]
        try:
            for x in self.products_before_sending:
                cursor.execute(f'select {current_month} from productos where id = {x}')
                current_sale = cursor.fetchall()[0][0]
                new_sale_state = current_sale + self.products_before_sending[x]
                cursor.execute(f'UPDATE productos SET {current_month} = {new_sale_state} WHERE id = {x}')
                conn.commit()
        except sqlite3.OperationalError:
            cursor.execute(f'ALTER TABLE productos ADD COLUMN {current_month} INTEGER DEFAULT 0')
            conn.commit()
            for x in self.products_before_sending:
                new_sale_state = current_sale + self.products_before_sending[x]
                cursor.execute(f'UPDATE productos SET {current_month} = {new_sale_state} WHERE id = {x}')
                conn.commit()
        self.products_before_sending = {}
        return self.sent_label.grid(row=6,column=0,sticky='w',padx=20,pady=20), self.total_label.grid_forget(),self.error_label.grid_forget(),self.bill_label.grid_forget(),self.no_stock_label.grid_forget()

app = Window()
menu_bar = tk.Menu(app)
options = tk.Menu(menu_bar,tearoff=0)

options.add_command(label="Ingresar producto",command=lambda:app.show(AddProduct))
options.add_command(label="Crear promociones",command=lambda:app.show(Offers))
options.add_command(label="Actualizar productos",command=lambda:app.show(Edit))
options.add_command(label="Eliminar productos",command=lambda:app.show(Delete))
menu_bar.add_cascade(label="Productos", menu=options)
menu_bar.add_command(label="Ventas",command=lambda:app.show(Sales))
menu_bar.add_command(label="Controlar precios",command=lambda:app.show(Prices))
menu_bar.add_command(label="Estadísticas",command=lambda:app.show(Statistics))
app.config(menu=menu_bar)
app.mainloop()