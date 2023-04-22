from tkinter import *
import tkintermapview

root = Tk()

root.title('Graph Theory')
root.geometry('900x700')

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(
    my_label, width=800, height=600, corner_radius=0)




def add_marker_event(coords):
    current_marker = 1
    print("Add marker:", coords)
    new_marker = map_widget.set_marker(
        coords[0], coords[1], text="Customer"+str(current_marker))
    current_marker += 1


map_widget.add_right_click_menu_command(label="Add Marker",
                                        command=add_marker_event,
                                        pass_coords=True)

map_widget.pack()


root.mainloop()
