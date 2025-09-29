import gi

from .function_block import FunctionBlock, ExecutionControlChart, State, Transition
from .ecc_renderer import EccRenderer
from .base import PageMixin

gi.require_version('Gtk', '4.0')
from gi.repository import Gio, Gdk, Gtk

class SimulatorEditor(PageMixin, Gtk.Box):
    fb : FunctionBlock
    ecc : ExecutionControlChart
    selected_state : State
    selected_transition : Transition
    def __init__(self, fb, current_tool=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fb = fb
        self.ecc = fb.get_ecc()
        self.current_tool = current_tool
        self.selected_state = None
        self.selected_action = None
        self.selected_transition = None
        self.enable_add = True # Controla a adicao de um novo estado

        # --------------- Control the main panels -----------------
        # Vertical panel
        self.paned_side = Gtk.Paned(wide_handle=False, orientation=Gtk.Orientation.VERTICAL, halign=Gtk.Align.FILL)
        # Horizontal panel
        self.paned = Gtk.Paned(wide_handle=True, orientation=Gtk.Orientation.HORIZONTAL)
        # ---------------------------------------------------------
        self.scrolled = Gtk.ScrolledWindow.new()
        self.ecc_render = EccRenderer(self.fb)
        self.gesture_press = Gtk.GestureClick.new()
        self.gesture_release = Gtk.GestureClick.new()
        self.event_controller = Gtk.EventControllerMotion.new()

        # Bottom box declaration
        self.box_bottom = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, halign=Gtk.Align.FILL, valign=Gtk.Align.FILL)
        self.box_bottom.set_homogeneous(True)

        # Side box declaration
        self.box_side = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, valign=Gtk.Align.FILL)

        # Create simulation box widgets
        self.build_simulation_panel()

        self.paned_side.set_vexpand(True)
        self.paned_side.set_hexpand(True)
        self.paned_side.set_start_child(self.scrolled)
        self.paned_side.set_resize_start_child(True)
        self.paned_side.set_shrink_start_child(False)
        self.paned_side.set_end_child(self.box_bottom)
        self.paned_side.set_resize_end_child(False)
        self.paned_side.set_shrink_end_child(False)
        self.scrolled.set_child(self.ecc_render)
        self.ecc_render.renderer_set_size_request(self.scrolled.get_allocation())

        self.paned.set_vexpand(True)
        self.paned.set_hexpand(True)
        self.paned.set_start_child(self.paned_side)
        self.paned.set_resize_start_child(True)
        self.paned.set_shrink_start_child(True)
        self.paned.set_end_child(self.box_side)
        self.paned.set_resize_end_child(False)
        self.paned.set_shrink_end_child(False)
        self.paned.set_position(2000)

        self.append(self.paned)

        # Call the method to update the simulation panel
        self.update_simulation_panel()

        # Gestures and controllers
        self.gesture_press.connect("pressed", self.button_press)
        self.gesture_release.connect("released", self.button_release)
        self.event_controller.connect("motion", self.motion_notify)
        self.ecc_render.add_controller(self.gesture_press)
        self.ecc_render.add_controller(self.gesture_release)
        self.ecc_render.add_controller(self.event_controller)
        self.cursor_crosshair = Gdk.Cursor.new_from_name("crosshair")
        self.ecc_render.set_cursor(self.cursor_crosshair)

        self.ecc_render.set_draw_func(self.on_draw, None)

    # -------------  ----------------

    def build_simulation_panel(self):
        title_label = Gtk.Label(label="Simulação do ECC", halign=Gtk.Align.CENTER)
        self.box_side.append(title_label)

        self.current_state_label = Gtk.Label(label="Estado Atual: N/A", halign=Gtk.Align.START)
        self.box_side.append(self.current_state_label)

        input_frame = Gtk.Frame(label="Entradas")
        self.input_grid = Gtk.Grid(column_spacing=10, row_spacing=5, margin_start=5, margin_end=5)
        input_frame.set_child(self.input_grid)
        self.box_side.append(input_frame)

        output_frame = Gtk.Frame(label="Saídas")
        self.output_grid = Gtk.Grid(column_spacing=10, row_spacing=5, margin_start=5, margin_end=5)
        output_frame.set_child(self.output_grid)
        self.box_side.append(output_frame)

        self.run_button = Gtk.Button(label="Executar ECC")
        self.run_button.connect("clicked", self.on_run_ecc)
        self.box_side.append(self.run_button)

    def update_simulation_panel(self):
        # Limpar grids antes de preenchê-los
        children_to_remove = list(self.input_grid.observe_children())
        for child in children_to_remove:
            if child is not None:
                self.input_grid.remove(child)

        children_to_remove = list(self.output_grid.observe_children())
        for child in children_to_remove:
            if child is not None:
                self.output_grid.remove(child)

        row = 0
        # Adicionar inputs (eventos e variáveis)
        self.input_widgets = {}
        for event in self.fb.events:
            if event.is_input:
                label = Gtk.Label(label=event.name, halign=Gtk.Align.START)
                button = Gtk.Button(label="Disparar")
                button.connect("clicked", self.on_run_ecc, event.name)
                self.input_grid.attach(label, 0, row, 1, 1)
                self.input_grid.attach(button, 1, row, 1, 1)
                row += 1

        for var in self.fb.variables:
            if var.is_input:
                label = Gtk.Label(label=var.name, halign=Gtk.Align.START)
                entry = Gtk.Entry()
                if var.value is not None:
                    entry.set_text(str(var.value))
                entry.connect("changed", self.on_variable_changed, var)
                self.input_grid.attach(label, 0, row, 1, 1)
                self.input_grid.attach(entry, 1, row, 1, 1)
                self.input_widgets[var.name] = entry
                row += 1

        row = 0
        # Adicionar outputs (eventos e variáveis)
        self.output_widgets = {}
        for event in self.fb.events:
            if not event.is_input:
                label = Gtk.Label(label=event.name, halign=Gtk.Align.START)
                state_label = Gtk.Label(label="Ativo" if event.active else "Inativo", halign=Gtk.Align.START)
                self.output_grid.attach(label, 0, row, 1, 1)
                self.output_grid.attach(state_label, 1, row, 1, 1)
                self.output_widgets[event.name] = state_label
                row += 1

        for var in self.fb.variables:
            if var.is_output:
                label = Gtk.Label(label=var.name, halign=Gtk.Align.START)
                value_label = Gtk.Label(label=str(var.value) if var.value is not None else "N/A", halign=Gtk.Align.START)
                self.output_grid.attach(label, 0, row, 1, 1)
                self.output_grid.attach(value_label, 1, row, 1, 1)
                self.output_widgets[var.name] = value_label
                row += 1

    def on_run_ecc(self, button, event_name=None):
        if not self.ecc.current_state:
            print("Nenhum estado inicial definido.")
            return

        print(f"Executando ECC com evento de entrada: '{event_name}'")
        self.ecc.execute_with_input(event_name)
        self.update_simulation_panel()
        self.update_bottom_treeview()

    def on_variable_changed(self, entry, variable):
        try:
            # Converte o valor de entrada para o tipo da variável
            new_value = entry.get_text()
            if variable.type:

                type_map = {
                    "BOOL": bool, "STRING": str, "REAL": float, "UINT": int, "ANY_ELEMENTARY": int, "TIME": float
                }
                var_type = type_map.get(variable.type, str)
                variable.value = var_type(new_value)
            else:
                variable.value = new_value
            print(f"Variável '{variable.name}' alterada para: {variable.value}")
        except ValueError:
            print(f"Entrada inválida. Digite um valor válido para o tipo '{variable.type}'.")

    def update_ecc_display(self):
        self.current_state_label.set_label(f"Estado Atual: {self.ecc.current_state.name}")
        self.update_simulation_panel()

    def on_row_selected_ecc(self, listbox, row):
        if row:
            '''
            label = row.get_child().get_label()
            state = self.ecc.state_get(label)
            self.ecc.current_state = state
            self.update_ecc_display()
            '''
            tree_path = row.get_path()
            tree_iter = self.states_liststore.get_iter(tree_path)
            state = self.states_liststore.get_value(tree_iter, 2)

            # Se o estado selecionado for diferente do anterior, atualize
            if self.selected_state != state:
                self.selected_state = state
                self.ecc.current_state = state
                self.update_bottom_treeview()
                self.trigger_change() # Dispara o redesenho apenas aqui

            # Atualiza o painel de simulação sem disparar o redesenho do ECC
            self.update_ecc_display()

    # --------------------------------------------------------------


    #  | ------------------------------------- |


    def on_draw(self, area, cr, wd, h, data):
        self.ecc_render.draw(area, cr, wd, h, data)

    # Redraw the ecc graph
    def trigger_change(self):
        self._changes_to_save = True
        self.ecc_render.queue_draw()

    def motion_notify(self, data, x, y):
        window = self.get_ancestor_window()
        tool_name = window.get_selected_tool()

        if tool_name == 'move':
            if not self.selected_state is None:
                #print(self.selected_state.x)
                self.selected_state.x = x-self.ecc_render.offset_x
                self.selected_state.y = y-self.ecc_render.offset_y
                self.trigger_change()
                self.update_scrolled_window()

    def button_press(self, e, data, x, y):
        window = self.get_ancestor_window()
        tool = window.get_selected_tool()
        print(f'tool = {tool}')
        if tool != 'add':
            state = self.ecc_render.get_state_at(x, y)

        if tool == 'add':
            # print('1')
            new_state = self.selected_state
            new_state.x = x
            new_state.y = y
            #self.ecc.state_add(new_state)
            self.update_side_treeview()
            self.update_bottom_treeview()
            self.trigger_change()
            self.selected_state = None
            self.enable_add = True
        elif tool == 'move':
            # print('2')
            self.selected_state = state
            self.update_bottom_treeview()
        elif tool == 'connect':
            if state is None:
                self.selected_state = None
                # print('3')
            else:
                if self.selected_state is None:
                    self.selected_state = state
                    # print(f'SELECTED = {self.selected_state.name}')
                    # print('4')
                else:
                    # print('5')
                    transition = Transition(self.selected_state, state)
                    self.ecc.transition_add(transition)
                    self.selected_state.transition_out_add(transition)
                    state.transition_in_add(transition)
                    self.trigger_change()
                    self.update_bottom_treeview()
                    self.selected_state = None
        elif tool == 'inspect':
            self.selected_state = state
            self.update_bottom_treeview()


    def button_release(self, e, data, x, y):
        window = self.get_ancestor_window()
        tool_name = window.get_selected_tool()

        if tool_name == 'move':
            self.update_scrolled_window()
            self.selected_state = None

    def update_scrolled_window(self):
        hadj = self.scrolled.get_hadjustment()
        vadj = self.scrolled.get_vadjustment()

        delta_x, delta_y = self.ecc_render.renderer_set_size_request(self.scrolled.get_allocation())

        hadj.set_value(hadj.get_value() + delta_x)
        vadj.set_value(vadj.get_value() + delta_y)
        self.scrolled.set_hadjustment(hadj)
        self.scrolled.set_vadjustment(vadj)
