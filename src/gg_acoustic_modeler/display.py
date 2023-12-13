from tkinter import ttk
from PIL import Image, ImageTk


class Display(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # message
        self.message_label = ttk.Label(self, text='', foreground='red')
        self.message_label.grid(row=1, column=0, columnspan=11)

        # save button
        self.import_button = ttk.Button(self, text='Import', command=self.import_clicked)
        self.import_button.grid(row=2, column=0, padx=10)

        # switch low mid high button
        self.switch_button = ttk.Button(self, text='Low', command=self.plot_clicked)
        self.switch_button.grid(row=3, column=0, padx=10)

        # switch merging button
        self.merge_button = ttk.Button(self, text='Split', command=self.merge_clicked)
        self.merge_button.grid(row=4, column=0, padx=10)

        self.length_label = ttk.Label(self, text='')
        self.length_label.grid(row=5, column=0, padx=10)

        self.max_res_label = ttk.Label(self, text='')
        self.max_res_label.grid(row=6, column=0, padx=10)

        self.difference = ttk.Label(self, text='')
        self.difference.grid(row=7, column=0, padx=10)

        self.waveform = ttk.Label(self)
        self.waveform.grid(row=2, column=1, columnspan=30, rowspan=30)

        self.spec = ttk.Label(self)
        self.spec.grid(row=2, column=31, columnspan=30, rowspan=30)

        self.rt60 = ttk.Label(self)
        self.rt60.grid(row=2, column=61, columnspan=30, rowspan=30)

        # set the controller
        self.controller = None

    def set_controller(self, controller):
        """
        Set the controller
        :param controller:
        :return:
        """

        self.controller = controller

    def import_clicked(self):
        """
        Handle import button click event
        :return:
        """

        if self.controller:
            self.controller.import_wav()

    def plot_clicked(self):
        """
        Handle plot button click event
        :return:
        """

        if self.controller:
            self.controller.change_plot_shown()

    def merge_clicked(self):
        """
        Handle merge button click event
        :return:
        """

        if self.controller:
            self.controller.change_plot_combined()

    def show_error(self, message):
        """
        Show an error message
        :param message:
        :return:
        """

        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """

        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def update_length(self, length):
        """
        updates the displayed length
        :param length:
        :return:
        """

        self.length_label['text'] = f"Duration: {length} s"

    def update_max_res(self, max_res):
        """
        updates the displayed max resonance
        :param max_res:
        :return:
        """

        self.max_res_label['text'] = f"Resonance: {max_res} Hz"

    def update_diff(self, diff):
        """
        updates the displayed difference
        :param diff:
        :return:
        """

        self.difference['text'] = f"Difference: {diff} s"

    def update_waveform(self):
        """
        updates the displayed waveform
        :param:
        :return:
        """

        new_image = ImageTk.PhotoImage(Image.open("waveform.png").resize((360, 240)))
        self.waveform.configure(image=new_image)
        self.waveform.image = new_image

    def update_spec(self):
        """
        updates the displayed spectrogram
        :param:
        :return:
        """

        new_image = ImageTk.PhotoImage(Image.open("spec.png").resize((360, 240)))
        self.spec.configure(image=new_image)
        self.spec.image = new_image

    def update_plot(self, plot, combined, name, imported):
        """
        updates the plot and merge buttons, plus the rt60 plot
        :param plot:
        :param combined:
        :param name:
        :param imported:
        :return:
        """

        name_1 = 'N/A'

        match plot:
            case 0:
                name_1 = 'Low'
            case 1:
                name_1 = 'Mid'
            case 2:
                name_1 = 'High'

        self.switch_button['text'] = name_1

        name_2 = 'N/A'

        match combined:
            case False:
                name_2 = 'Split'
            case True:
                name_2 = 'Merged'

        self.merge_button['text'] = name_2

        filename = ''
        if not combined:
            filename = name[plot]
        else:
            filename = 'rt60_combined.png'

        if imported:
            new_image = ImageTk.PhotoImage(Image.open(filename).resize((360, 240)))
            self.rt60.configure(image=new_image)
            self.rt60.image = new_image

    def hide_message(self):
        """
        Hide the message
        :return:
        """

        self.message_label['text'] = ''


