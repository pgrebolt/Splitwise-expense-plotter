import gui_assembler

def change_language(event, root, lang):

    selected_language = lang # Llegim el nou idioma

    # Netegem els frames
    frames = root.winfo_children() # Frames dins la finestra principal
    for frame in frames: # Per cada frame
        for widget in frame.winfo_children(): # Per cada widget al frame
            widget.destroy() # Treure widget


    frame_input, frame_categories, frame_plot = gui_ensambler.create_frames(root)

    # Muntem la finestra un altre cop
    gui_ensambler.create_inputs(frame_input, selected_language)
    altres_var, histogram_var, checkbox_vars = gui_ensambler.create_categories(frame_categories, selected_language)
    gui_ensambler.create_commander(frame_plot, lang, file_entry, save_entry, altres_var, histogram_var, checkbox_vars)
