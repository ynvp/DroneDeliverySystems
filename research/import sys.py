import sys
import tkinter
import tkinter.messagebox
from tkinter import ttk
from tkintermapview import TkinterMapView
import run as r
import weight_dialog as wd
import current_location as cl


class App(tkinter.Tk,):
    APP_NAME = "Drone Delivery System"

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry("%dx%d" % (width, height))
        self.state('zoomed')

        # self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Return>", self.search)

        if sys.platform == "darwin":
            self.bind("<Command-q>", self.on_closing)
            self.bind("<Command-w>", self.on_closing)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3)
        self.grid_rowconfigure(0)

        self.search_bar = tkinter.Entry(self, width=50)
        self.search_bar.grid(row=0, column=0, pady=10, padx=10, sticky="we")
        self.search_bar.focus()

        self.search_bar_button = tkinter.Button(
            master=self, width=8, text="Search", command=self.search)
        self.search_bar_button.grid(row=0, column=1, pady=10, padx=10)

        self.search_bar_clear = tkinter.Button(
            master=self, width=8, text="Clear", command=self.clear)
        self.search_bar_clear.grid(row=0, column=2, pady=10, padx=10)

        self.map_widget = TkinterMapView(
            width=self.winfo_screenwidth(), height=600, corner_radius=0)
        self.map_widget.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.marker_list_box = tkinter.Listbox(self, height=8)
        self.marker_list_box.grid(
            row=2, column=0, sticky="ew", padx=10, pady=10)

        self.listbox_button_frame = tkinter.Frame(master=self)
        self.listbox_button_frame.grid(
            row=2, column=1, sticky="nsew")

        self.listbox_button_frame.grid_columnconfigure(0, weight=1)

        self.algo_btn = tkinter.Button(master=self.listbox_button_frame, width=20, text="Calculate Path",
                                       bg="green", fg="white", command=self.run)
        self.algo_btn.grid(row=0, column=0, pady=10, padx=10)

        self.connect_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="connect marker with path",
                                                    command=self.connect_marker_products)
        self.connect_marker_button.grid(row=1, column=0, pady=10, padx=10)

        self.clear_marker_button = tkinter.Button(master=self.listbox_button_frame, width=20, text="clear marker list",
                                                  command=self.clear_marker_list)
        self.clear_marker_button.grid(row=2, column=0, pady=10, padx=10)
        self.map_widget.set_address("NYC")

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
        self.map_widget.add_left_click_map_command(self.delete_last_marker)
        self.current_customer_counter = 1
        self.current_warehouse_counter = 1
        self.current_charging_point_counter = 1
        self.current_warehouse_marker = None

        # self.default_warehouse_marker = self.map_widget.set_marker(
        #     40.7194939, - 74.0767397, text="Warehouse1", text_color="green")
        # self.warehouse_marker_list.append(self.default_warehouse_marker)

    def run(self):
        if len(r.warehouses) > 0 and len(r.package_weights) > 0:
            if len(r.charging_points) > 0:
                tkinter.messagebox.showwarning(
                    'warning', 'Charging points were not added. This may affect path.')
            self.inputDialog = cl.CurrentLocation(self.tk)
            self.wait_window(self.inputDialog.top)
            print('log: current location - ', self.inputDialog.location)
            self.formatted_warehouses = dict([(location[0], location[1])
                                              for location in r.warehouses])

            marker_list_warehouses = dict([(warehouse.text.split(
                '\n')[0], warehouse) for warehouse in self.warehouse_marker_list])
            print('log: ', marker_list_warehouses)
            self.current_warehouse_marker = marker_list_warehouses[
                self.inputDialog.location]
            current_loc = self.formatted_warehouses[self.inputDialog.location]
            if (current_loc == None):
                tkinter.messagebox.showerror(
                    'error', 'No current location set!.')
            self.final_path = r.deliver_packages(
                [self.inputDialog.location, current_loc])
            r.selected_packages = []
        else:
            if len(r.warehouses) == 0:
                tkinter.messagebox.showerror(
                    'error', 'Warehouses not yet added!')
                print('Log: warehouses not yet added')
            if len(r.package_weights) == 0:
                tkinter.messagebox.showerror(
                    'error', 'Packages not yet added!')
                print('Log: Packages not yet added')

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
        r.delivery_locations.append(
            ["Customer"+str(self.current_customer_counter), (coords[0], coords[1])])
        self.marker_list_box.insert(
            tkinter.END, "Customer " + str(self.current_customer_counter) + " - Package weight: "+self.inputDialog.weight)
        self.marker_list_box.see(tkinter.END)
        self.current_customer_counter += 1
        self.marker_list.append(new_marker)
        self.search_marker = new_marker

    def add_warehouse_marker_event(self, coords):
        print("Added warehouse location:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="Warehouse" + str(self.current_warehouse_counter), text_color="green")
        r.warehouses.append(
            ["Warehouse"+str(self.current_warehouse_counter), (coords[0], coords[1])])
        self.marker_list_box.insert(
            tkinter.END, "Warehouse" + str(self.current_warehouse_counter))
        self.marker_list_box.see(tkinter.END)
        self.current_warehouse_counter += 1
        self.warehouse_marker_list.append(new_marker)
        self.search_marker = new_marker

    def add_charging_point_marker_event(self, coords):
        print("Added Charging Point marker:", coords)
        new_marker = self.map_widget.set_marker(
            coords[0], coords[1], text="ChargingPoint" +
            str(self.current_charging_point_counter))
        r.charging_points.append(
            ["ChargingPoint"+str(self.current_charging_point_counter), (coords[0], coords[1])])
        self.marker_list_box.insert(
            tkinter.END, "ChargingPoint"+str(self.current_charging_point_counter))
        self.marker_list_box.see(tkinter.END)
        self.current_charging_point_counter += 1
        self.charging_points_marker_list.append(new_marker)
        self.search_marker = new_marker

    def assign_weight(self, customer, weight):
        r.package_weights.append([customer, int(weight)])
        print('log: Product weight assigned successfully!')
        print(r.package_weights)

    def delete_last_marker(self, coords):
        if (len(self.map_widget.canvas_marker_list) > 0):
            self.last_element = self.map_widget.canvas_marker_list.pop()
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

    # Button deleted
    def save_marker(self):
        if self.search_marker is not None:
            self.marker_list_box.insert(
                tkinter.END, f" {len(self.marker_list)}. {self.search_marker.text} ")
            self.marker_list_box.see(tkinter.END)
            self.marker_list.append(self.search_marker)

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
        self.connect_marker()
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
        if self.current_warehouse_marker != None:
            position_list.append(self.current_warehouse_marker.position)
            marker_list_customers = dict([(customer.text.split(
                '\n')[0], customer) for customer in self.marker_list])
            print(marker_list_customers)
            for package in self.final_path:
                if package in marker_list_customers:
                    marker = marker_list_customers[package]
                    print(marker)
                    position_list.append(marker.position)

            if self.marker_path is not None:
                self.map_widget.delete(self.marker_path)

            print(position_list)

            if len(position_list) > 0:
                self.marker_path = self.map_widget.set_path(position_list)
            r.selected_packages_copy.clear()
        else:
            tkinter.messagebox.showerror(
                'error', 'Please click on Give Path button!')

    # Inbuilt marker connector function
    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:

            position_list.append(marker.position)

        if self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def clear(self):
        self.search_bar.delete(0, last=tkinter.END)
        self.map_widget.delete(self.search_marker)

    def on_closing(self, event=0):
        self.destroy()
        exit()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
