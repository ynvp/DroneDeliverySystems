import sys
import customtkinter
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
import run as r
import weight_dialog as wd
import current_location as cl
from tkinter import *

customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    APP_NAME = "Drone Delivery System"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(self.APP_NAME)

        self.after(0, lambda: self.state('zoomed'))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(
            master=self, width=150, corner_radius=0, fg_color=None)
        self.frame_left.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self.frame_right = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame_right.grid(row=0, column=1, rowspan=1,
                              pady=0, padx=0, sticky="nsew")

        # ============ frame_left ============

        self.frame_left.grid_rowconfigure(2, weight=1)

        self.calculate_path_button = customtkinter.CTkButton(
            master=self.frame_left, text="Calculate Path", command=self.run)
        self.calculate_path_button.grid(
            pady=(20, 0), padx=(20, 20), row=0, column=0)

        self.clear_marker_button = customtkinter.CTkButton(master=self.frame_left, text="Clear locations",
                                                           command=self.clear_marker_list)
        self.clear_marker_button.grid(
            pady=(20, 0), padx=(20, 20), row=1, column=0)

        self.marker_list_box_scrollbar = Scrollbar(
            self.frame_left, orient=tkinter.HORIZONTAL)
        self.marker_list_box = tkinter.Listbox(
            self.frame_left, height=40, width=40, fg='white', bg='black', xscrollcommand=self.marker_list_box_scrollbar.set)
        self.marker_list_box_scrollbar.config(
            command=self.marker_list_box.xview)
        self.marker_list_box.grid(
            pady=(5, 0), padx=(1, 1), row=2, column=0)
        self.marker_list_box_scrollbar.grid(column=0, row=3)

        self.map_label = customtkinter.CTkLabel(
            self.frame_left, text="Tile Server:", anchor="w")
        self.map_label.grid(row=3, column=0, padx=(20, 20), pady=(20, 0))
        self.map_option_menu = customtkinter.CTkOptionMenu(self.frame_left, values=["OpenStreetMap", "Google normal", "Google satellite"],
                                                           command=self.change_map)
        self.map_option_menu.grid(row=4, column=0, padx=(20, 20), pady=(10, 0))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.frame_left, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(
            row=5, column=0, padx=(20, 20), pady=(20, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame_left, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=(20, 20), pady=(10, 20))

        # ============ frame_right ============

        self.frame_right.grid_rowconfigure(1, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=0)
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_columnconfigure(1, weight=0)
        self.frame_right.grid_columnconfigure(2, weight=1)

        self.map_widget = TkinterMapView(self.frame_right, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0,
                             columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))

        self.search_bar = customtkinter.CTkEntry(master=self.frame_right,
                                                 placeholder_text="Type address")
        self.search_bar.grid(row=0, column=0, sticky="we",
                             padx=(12, 0), pady=12)

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Search",
                                                width=90,
                                                command=self.search)
        self.button_5.grid(row=0, column=1, sticky="w", padx=(12, 0), pady=12)

        self.map_widget.set_address("NYC")
        self.map_option_menu.set("OpenStreetMap")
        self.appearance_mode_optionemenu.set("Dark")

        self.marker_list = []
        self.warehouse_marker_list = []
        self.charging_points_marker_list = []
        self.marker_path = None
        self.final_path = None
        self.search_marker = None
        self.search_in_progress = False
        self.map_widget.add_right_click_menu_command(label="Add Customer",
                                                     command=self.add_customer_marker_event,
                                                     pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="Add Warehouse",
                                                     command=self.add_warehouse_marker_event,
                                                     pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="Add Charging Point",
                                                     command=self.add_charging_point_marker_event,
                                                     pass_coords=True)
        self.map_widget.add_right_click_menu_command(label="Delete last added location",
                                                     command=self.delete_last_marker,
                                                     pass_coords=True)
        self.map_widget.add_left_click_map_command(
            self.add_charging_point_marker_event)
        self.current_customer_counter = 1
        self.current_warehouse_counter = 1
        self.current_charging_point_counter = 1
        self.current_warehouse_marker = None

    def run(self):
        if len(r.warehouses) > 0 and len(r.package_weights) > 0 and len(r.charging_points) > 0:
            self.inputDialog = cl.CurrentLocation(self)
            self.wait_window(self.inputDialog.top)
            print('log: current location - ', self.inputDialog.location)
            self.formatted_warehouses = list(r.warehouses.keys())
            print(self.formatted_warehouses)

            marker_list_warehouses = dict([(warehouse.text.split(
                '\n')[0], warehouse) for warehouse in self.warehouse_marker_list])
            print('log: ', marker_list_warehouses)
            self.current_warehouse_marker = marker_list_warehouses[
                self.inputDialog.location]
            current_loc = r.warehouses[self.inputDialog.location]
            if (current_loc == None):
                tkinter.messagebox.showerror(
                    'error', 'No current location set!.')
            self.final_path = r.deliver_packages(
                [self.inputDialog.location, current_loc])
            print(self.final_path)
            r.selected_packages = []
            self.display_calculated_data()
            self.connect_marker_products()
        else:
            if len(r.warehouses) == 0:
                tkinter.messagebox.showerror(
                    'error', 'Warehouses not yet added!')
                print('Log: warehouses not yet added')
            if len(r.package_weights) == 0:
                tkinter.messagebox.showerror(
                    'error', 'Packages not yet added!')
                print('Log: Packages not yet added')
            if len(r.charging_points) == 0:
                tkinter.messagebox.showwarning(
                    'warning', 'Charging points were not added. This may affect path. Exiting calculation.')
                print('Log: Charging points not yet added')

    def add_customer_marker_event(self, coords):
        self.inputDialog = wd.WeightDialog(self)
        self.wait_window(self.inputDialog.top)
        print('log: weight: ', self.inputDialog.weight)
        print("log: Added customer marker:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="Customer" +
            str(self.current_customer_counter) +
            '\n Package weight: '+self.inputDialog.weight,
            command=self.assign_weight("Customer"+str(self.current_customer_counter), self.inputDialog.weight))
        # r.delivery_locations.append(
        #     ["Customer"+str(self.current_customer_counter), (coords[0], coords[1])])
        r.delivery_locations['Customer' +
                             str(self.current_customer_counter)] = (coords[0], coords[1])
        self.marker_list_box.insert(
            tkinter.END, "Customer " + str(self.current_customer_counter) + " with Package weight: "+self.inputDialog.weight+" added")
        self.marker_list_box.see(tkinter.END)
        self.current_customer_counter += 1
        self.marker_list.append(new_marker)
        self.search_marker = new_marker

    def assign_weight(self, customer, weight):
        r.package_weights[customer] = int(weight)
        print('log: Product weight assigned successfully!')
        print(r.package_weights)

    def add_warehouse_marker_event(self, coords):
        print("Added warehouse location:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="Warehouse" + str(self.current_warehouse_counter), text_color="green")
        r.warehouses["Warehouse" +
                     str(self.current_warehouse_counter)] = (coords[0], coords[1])
        self.marker_list_box.insert(
            tkinter.END, "Warehouse " + str(self.current_warehouse_counter)+" added")
        self.marker_list_box.see(tkinter.END)
        self.current_warehouse_counter += 1
        self.warehouse_marker_list.append(new_marker)
        self.search_marker = new_marker

    def add_charging_point_marker_event(self, coords):
        print("Added Charging Point marker:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="ChargingPoint" +
            str(self.current_charging_point_counter))
        r.charging_points["ChargingPoint" +
                          str(self.current_charging_point_counter)] = (coords[0], coords[1])
        self.marker_list_box.insert(
            tkinter.END, "ChargingPoint "+str(self.current_charging_point_counter)+" added")
        self.marker_list_box.see(tkinter.END)
        self.current_charging_point_counter += 1
        self.charging_points_marker_list.append(new_marker)
        self.search_marker = new_marker

    def delete_last_marker(self, coords):
        if (len(self.map_widget.canvas_marker_list) > 0):
            self.last_element = self.map_widget.canvas_marker_list.pop()
            # counter decrement
            if 'Warehouse' in self.last_element.text:
                self.current_warehouse_counter -= 1
            if 'Customer' in self.last_element.text:
                self.current_customer_counter -= 1
            if 'Charging' in self.last_element.text:
                self.current_charging_point_counter -= 1
            self.marker_list_box.insert(
                tkinter.END, self.last_element.text+" deleted")
            print('log: Element deleted successfully!')
            self.last_element.delete()
        else:
            print('No locations added yet!')
            tkinter.messagebox.showerror('error', 'No locations added yet!')

    def search(self, event=None):
        if not self.search_in_progress:
            self.search_in_progress = True
            if self.search_marker not in self.marker_list:
                self.map_widget.delete(self.search_marker)

            address = self.search_bar.get()
            self.search_marker = self.map_widget.set_address(
                address, marker=True)
            if self.search_marker is False:
                # address was invalid (return value is False)
                self.search_marker = None
            self.search_in_progress = False

    def clear_marker_list(self):
        for marker in self.marker_list:
            self.map_widget.delete(marker)
        for marker in self.warehouse_marker_list:
            self.map_widget.delete(marker)
        for marker in self.charging_points_marker_list:
            self.map_widget.delete(marker)

        self.marker_list_box.delete(0, tkinter.END)
        self.marker_list.clear()
        self.warehouse_marker_list.clear()
        self.charging_points_marker_list.clear()
        r.delivery_locations.clear()
        r.selected_packages.clear()
        r.selected_packages_copy.clear()
        if self.final_path != None:
            self.final_path.clear()
        self.current_warehouse_counter = 1
        self.current_customer_counter = 1
        self.current_charging_point_counter = 1

    # Modified marker connector function
    def connect_marker_products(self):
        position_list = []
        # if self.current_warehouse_marker != None:
        position_list.append(self.current_warehouse_marker.position)
        marker_list_combined = dict([(customer.text.split(
            '\n')[0], customer) for customer in self.marker_list])
        marker_list_combined.update(dict(
            [(cp.text, cp) for cp in self.charging_points_marker_list]))
        marker_list_combined.update(dict(
            [(w.text, w) for w in self.warehouse_marker_list]))
        # print(marker_list_combined)
        for package in self.final_path:
            if package in marker_list_combined:
                marker = marker_list_combined[package]
                print(marker)
                position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        # print(position_list)
        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)
        r.selected_packages_copy.clear()
        # else:
        #     tkinter.messagebox.showerror(
        #         'error', 'Please click on Calculate Path button!')

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def display_calculated_data(self):
        p = ''
        for i in self.final_path:
            p += i+'-->'
        self.marker_list_box.insert(
            tkinter.END, p[:-3])

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_map(self, new_map: str):
        if new_map == "OpenStreetMap":
            self.map_widget.set_tile_server(
                "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
        elif new_map == "Google normal":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        elif new_map == "Google satellite":
            self.map_widget.set_tile_server(
                "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
