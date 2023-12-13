class Controller:
    def __init__(self, model, display):
        self.model = model
        self.display = display

    def import_wav(self):
        """
        Sets the file to import
        :return:
        """

        try:
            # import the model
            self.model.import_wav()
            # show a success message
            self.display.show_success(f'File {self.model.filepath} has been imported.')
            self.model.imported = True
            self.display.update_length(self.model.length)
            self.display.update_max_res(self.model.max_res)
            self.display.update_diff(self.model.avg_diff)
            self.display.update_waveform()
            self.display.update_spec()
            self.display.update_plot(self.model.plot_shown, self.model.plot_combined, self.model.plot_name,
                                     self.model.imported)
        except ValueError as error:
            # show an error message
            self.display.show_error(error)

    def change_plot_shown(self):
        if self.model.plot_shown < 2:
            self.model.plot_shown += 1
        else:
            self.model.plot_shown = 0

        self.display.update_plot(self.model.plot_shown, self.model.plot_combined, self.model.plot_name,
                                     self.model.imported)

    def change_plot_combined(self):
        self.model.plot_combined = not self.model.plot_combined

        self.display.update_plot(self.model.plot_shown, self.model.plot_combined, self.model.plot_name,
                                 self.model.imported)

