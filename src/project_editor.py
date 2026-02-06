from gi.repository import Adw
from gi.repository import Gtk
from gi.repository import Gio
from gi.repository import GLib

from base import PageMixin
from system_editor import SystemEditor
from system_config_editor import SystemConfigEditor
from fb_editor import FunctionBlockEditor
from export import ExportWindow

@Gtk.Template(resource_path='/com/lapas/Fbe/menu.ui')
class ProjectEditor(PageMixin, Gtk.Box):
    __gtype_name__ = 'ProjectEditor'
    
    project_menu_button = Gtk.Template.Child()
    primary_menu = Gtk.Template.Child()
    sys_config_submenu = Gtk.Template.Child()
    apps_submenu = Gtk.Template.Child()
    popover_menubar = Gtk.Template.Child()
    
    def __init__(self, window, system=None, current_page=None, current_tool=None, library=None, system_editor=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.window = window
        self.system = system
        self.library = library
        self.editor_index = 0
        self.current_page = current_page 
        self.current_page_label = Gtk.Label()
        self.last_page = None
        self.last_page_label = None
        self.current_tool = current_tool
        self.system_editor = SystemEditor(self.window, self, self.system)
        self.system_configuration_editor = SystemConfigEditor(self.system, self, self.library)
        self.applications_editors = list()
        
        if current_page is None:
            self.current_page = self.system_editor  # Always open in system editor 
            self.current_page_label.set_label('System Information')
        
        self.open_menu = Gio.Menu.new()
        self.project_bar = Gtk.ActionBar(valign=Gtk.Align.START)
        self.vpaned = Gtk.Paned(wide_handle=False, orientation = Gtk.Orientation.VERTICAL)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        self.vpaned.set_start_child(self.project_bar)
        self.vpaned.set_resize_start_child(False)
        self.vpaned.set_end_child(self.current_page)
        self.vpaned.set_resize_end_child(True)
        self.vpaned.set_shrink_end_child(False)
        self.vbox.append(self.vpaned)
        self.vbox.set_vexpand(True)
        self.vbox.set_hexpand(True)
        self.append(self.vbox)
        
        self.project_menu_button.set_label('THIS PROJECT')
        
        self._create_action("export-project", self.on_export_project)
        self._create_action("system-information", self.on_system_information)
        self._create_action("system-configuration", self.on_system_configuration)
        self._create_action("apps-swipe-left", self.on_apps_swipe_left)
        self._create_action("apps-swipe-right", self.on_apps_swipe_right)
        self._create_action("last-page", self.goto_last_page)
        self._create_action("open-simulator-dialog", self.on_open_simulator_dialog)
        
        self.build_application_menu()
        self.build_system_config_menu()
            
        self.project_bar.pack_start(self.project_menu_button)
        self.project_bar.pack_start(self.current_page_label)
          
    # -------------- Methods to create actions ----------------------
    def _create_action(self, action_name, callback, *args):
        action = Gio.SimpleAction.new(action_name, None)
        if not args:
            action.connect("activate", callback)
            self.window.add_action(action)
        else:
            action.connect("activate", callback, args)
            self.window.add_action(action)
    
    def _action_append_menu(self, menu, elem, suffix, callback):
        label = elem.name
        action_label = label+suffix
        self._create_action(action_label, callback, elem)
        menu.append(label, "win."+action_label)
    # ---------------------------------------------------------------
        
    # System configuration method
    def build_system_config_menu(self):
        for dev in self.system.devices:
            self._action_append_menu(self.sys_config_submenu, dev, '-dev', self.on_application_editor)
            # label = dev.name
            # label_action = label+"-dev"
            # self._create_action(label_action, self.on_application_editor)
            # self.sys_config_submenu.append(label, "win."+label_action)
            print('')
    
    def update_system_config_menu(self):
        self.sys_config_submenu.remove_all()
        for dev in self.system.devices:
            label = dev.name
            label_action = label+"-dev"
            self.sys_config_submenu.append(label, "win."+label_action)
            
    def build_application_menu(self):       
        for app in self.system.applications:
            self.applications_editors.append(FunctionBlockEditor(app, project=self, window=self.window))
            self._action_append_menu(self.apps_submenu, app, '-app', self.on_application_editor)
            # label = app.name
            # label_action = label+"-app"
            # self._create_action(label_action, self.on_application_editor, app)
            # self.apps_submenu.append(label, "win."+label_action) 
    
    def update_application_menu(self):
        self.applications_editors.clear()
        self.apps_submenu.remove_all()
        for app in self.system.applications:
            self.applications_editors.append(FunctionBlockEditor(app, project=self))
            label = app.name
            label_action = label+"-app"
            self.apps_submenu.append(label, "win."+label_action)
            
    def on_system_information(self, action, param=None):
        self.last_page = self.current_page
        self.last_page_label = self.current_page_label.get_label()
        self.current_page_label.set_label('System Information')
        self.current_page = self.system_editor
        self.vpaned.set_end_child(self.current_page)
        
    def on_system_configuration(self, action, param=None):
        self.last_page = self.current_page
        self.last_page_label = self.current_page_label.get_label()
        self.current_page_label.set_label('System Configuration')
        self.current_page = self.system_configuration_editor
        self.vpaned.set_end_child(self.current_page)
    
    def on_apps_swipe_left(self, action, param=None):
        if self.editor_index == 0:
            self.editor_index = len(self.applications_editors)-1
        else:
            self.editor_index -= 1
        self.last_page = self.current_page
        self.last_page_label = self.current_page_label.get_label()
        self.current_page_label.set_label(self.applications_editors[self.editor_index].app.name)
        self.current_page = self.applications_editors[self.editor_index]
        self.vpaned.set_end_child(self.current_page)
            
    def on_apps_swipe_right(self, action, param=None):
        self.editor_index += 1
        if self.editor_index == len(self.applications_editors):
            self.editor_index = 0
        self.last_page = self.current_page
        self.last_page_label = self.current_page_label.get_label()
        self.current_page_label.set_label(self.applications_editors[self.editor_index].app.name)
        self.current_page = self.applications_editors[self.editor_index]
        self.vpaned.set_end_child(self.current_page)

    def on_application_editor(self, action, param=None, app=None):
        if isinstance(app, tuple):
            app_editor = self.application_editor_get(app[0])
        else:
            app_editor = self.application_editor_get(app)
        self.last_page = self.current_page
        self.current_page_label.set_label(app_editor.app.name)
        self.current_page = app_editor
        self.vpaned.set_end_child(self.current_page)
    
    def application_editor_get(self, app):
        for editor in self.applications_editors:
            if editor.app.name == app.name:
                return editor
        return None

    def on_device_editor(self, project):
        dev_editor = SystemConfigEditor(system = self.system, project = project, library=self.library)
        self.last_page = self.current_page
        self.current_page = dev_editor
        self.vpaned.set_end_child(self.current_page)

    def on_resource_editor(self, resource, project):
        resource_editor = FunctionBlockEditor(fb_diagram=resource.fb_network, project=project)
        self.last_page = self.current_page
        self.current_page = resource_editor
        self.vpaned.set_end_child(self.current_page)

    def goto_last_page(self, action, param=None):
        if self.last_page is not None:
            current_page_label = self.current_page_label.get_label()
            current_page = self.current_page
            self.current_page = self.last_page
            self.current_page_label.set_label(self.last_page_label)
            self.last_page = current_page
            self.last_page_label = current_page_label
            self.vpaned.set_end_child(self.current_page)
            
    # Project exportation method
    def on_export_project(self, action, param=None):
        self.last_page = self.current_page
        self.last_page_label = self.current_page_label.get_label()
        self.current_page = ExportWindow(self.system, self.window)
        self.current_page_label.set_label("Export project")
        self.vpaned.set_end_child(self.current_page)
        
    def update_system_editor(self):
        self.system_editor.update_application_list()

    def save_file_dialog(self, action, _):
        self._native = Gtk.FileChooserNative(
            title="Save File As",
            transient_for=self,
            action=Gtk.FileChooserAction.SAVE,
            accept_label="_Save",
            cancel_label="_Cancel",
        )
        self._native.connect("response", self.on_save_response)
        self._native.show()

    def on_save_response(self, native, response):
        if response == Gtk.ResponseType.ACCEPT:
            self.save_file(native.get_file())
        self._native = None

    def save_file(self, file):
        buffer = self.main_text_view.get_buffer()

        # Retrieve the iterator at the start of the buffer
        start = buffer.get_start_iter()
        # Retrieve the iterator at the end of the buffer
        end = buffer.get_end_iter()
        # Retrieve all the visible text between the two bounds
        text = buffer.get_text(start, end, False)

        # If there is nothing to save, return early
        if not text:
            return

        bytes = GLib.Bytes.new(text.encode('utf-8'))

        # Start the asynchronous operation to save the data into the file
        file.replace_contents_bytes_async(
            bytes,
            None,
            False,
            Gio.FileCreateFlags.NONE,
            None,
            self.save_file_complete
        )

    def save_file_complete(self, file, result):
        res = file.replace_contents_finish(result)
        info = file.query_info("standard::display-name",
                               Gio.FileQueryInfoFlags.NONE)
        if info:
            display_name = info.get_attribute_string("standard::display-name")
        else:
            display_name = file.get_basename()

        if not res:
            msg = f"Unable to save as “{display_name}”"
        else:
            msg = f"Saves as “{display_name}”"
        self.toast_overlay.add_toast(Adw.Toast(title=msg))

    def save(self, file_path_name=None):
        status = self.selected_fb.save(file_path_name)
        if status == True:
            self._changes_to_save = False
        return status

    def has_file_path_name(self):
        return self.selected_fb.get_file_path_name() is not None

    def get_tab_name(self):
        if self.selected_fb is not None:
            return self.selected_fb.get_name()
        return self

    # -------------- Métodos do Simulador ----------------------

    def get_available_fbs(self):
        """Retorna uma lista de todos os FBs disponíveis no projeto"""
        available_fbs = []

        # Coletar FBs das aplicações
        for app in self.system.applications:
            if hasattr(app, 'fb_network') and app.fb_network:
                for fb_instance in app.fb_network.function_blocks:
                    available_fbs.append({
                        'name': f"{app.name} / {fb_instance.name}",
                        'fb': fb_instance,
                        'type': 'application'
                    })

        # Coletar FBs dos devices/resources
        if hasattr(self.system, 'devices'):
            for device in self.system.devices:
                if hasattr(device, 'resources'):
                    for resource in device.resources:
                        if hasattr(resource, 'fb_network') and resource.fb_network:
                            for fb_instance in resource.fb_network.function_blocks:
                                available_fbs.append({
                                    'name': f"{device.name} / {resource.name} / {fb_instance.name}",
                                    'fb': fb_instance,
                                    'type': 'resource'
                                })

        return available_fbs

    def on_open_simulator_dialog(self, action, param=None):
        """Mostra um diálogo para selecionar qual FB simular"""
        available_fbs = self.get_available_fbs()

        if not available_fbs:
            # Mostrar mensagem de erro se não houver FBs disponíveis
            dialog = Adw.MessageDialog(
                transient_for=self.window,
                heading="Nenhum Function Block Disponível",
                body="Não há Function Blocks disponíveis no projeto para simular. Adicione FBs às aplicações primeiro.",
            )
            dialog.add_response("ok", "OK")
            dialog.present()
            return

        # Criar diálogo de seleção
        dialog = Adw.MessageDialog(
            transient_for=self.window,
            heading="Selecionar Function Block para Simular",
            body="Escolha qual Function Block você deseja simular:",
        )

        # Criar uma lista de opções
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)

        for fb_info in available_fbs:
            row = Gtk.ListBoxRow()
            label = Gtk.Label(label=fb_info['name'], xalign=0)
            label.set_margin_start(10)
            label.set_margin_end(10)
            label.set_margin_top(5)
            label.set_margin_bottom(5)
            row.set_child(label)
            row.fb_info = fb_info  # Armazenar informação do FB na row
            listbox.append(row)

        # Selecionar o primeiro item por padrão
        listbox.select_row(listbox.get_row_at_index(0))

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(listbox)
        scrolled.set_min_content_height(200)
        scrolled.set_min_content_width(300)
        scrolled.set_max_content_height(400)

        dialog.set_extra_child(scrolled)
        dialog.add_response("cancel", "Cancelar")
        dialog.add_response("open", "Abrir Simulador")
        dialog.set_response_appearance("open", Adw.ResponseAppearance.SUGGESTED)

        dialog.connect("response", self.on_simulator_dialog_response, listbox)
        dialog.present()

    def on_simulator_dialog_response(self, dialog, response, listbox):
        """Callback quando o usuário responde ao diálogo de seleção"""
        if response == "open":
            selected_row = listbox.get_selected_row()
            if selected_row:
                fb_info = selected_row.fb_info
                self.open_simulator_with_fb(fb_info['fb'], fb_info['name'])

    def open_simulator_with_fb(self, fb, fb_name):
        """Abre o simulador com o FB especificado"""
        from simulator_editor import SimulatorEditor

        # Verificar se já existe uma aba do simulador para este FB
        notebook = self.window.notebook
        simulator_widget = None

        for i in range(notebook.get_n_pages()):
            page_widget = notebook.get_nth_page(i)
            if isinstance(page_widget, SimulatorEditor):
                # Verificar se é o mesmo FB
                if page_widget.fb.name == fb.name:
                    simulator_widget = page_widget
                    break

        # Se já existe, navegar para ela
        if simulator_widget:
            page_num = notebook.page_num(simulator_widget)
            notebook.set_current_page(page_num)
        else:
            # Criar nova aba do simulador
            simulator_editor = SimulatorEditor(fb)
            page_num = notebook.insert_page(
                simulator_editor,
                Gtk.Label.new(f"Simulador: {fb_name}"),
                -1
            )
            notebook.set_current_page(page_num)
            notebook.set_tab_detachable(simulator_editor, True)
            notebook.set_visible(True)

