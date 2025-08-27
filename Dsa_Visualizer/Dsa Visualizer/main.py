import pygame
import random
import asyncio
from state_manager import StateManager
from ui_elements.button import Button
from ui_elements.inputbox import InputBox
from ui_elements.panel import CodePanel
# Data Structures
from visualizers.bst_visualizer import BSTVisualizer
from visualizers.rb_tree_visualizer import RBTreeVisualizer
from visualizers.queue_visualizer import QueueVisualizer
from visualizers.stack_visualizer import StackVisualizer
from visualizers.linked_list_visualizer import LinkedListVisualizer
from visualizers.heap_visualizer import MinHeapVisualizer
from visualizers.array_visualizer import ArrayVisualizer
from visualizers.trie_visualizer import TrieVisualizer
# Algorithms
from visualizers.sorting_visualizer import SortingVisualizer
from visualizers.searching_visualizer import SearchingVisualizer

# --- Initialization & Constants ---
pygame.init(); pygame.mixer.init(); pygame.font.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)); pygame.display.set_caption("DSA Visualizer"); clock = pygame.time.Clock()

# --- THEMES ---
THEMES = {
    'dark': { 'bg': (30, 30, 40), 'text': (220, 220, 220), 'primary': (100, 100, 100), 'hover': (150, 150, 150),
              'accent1': (0, 150, 150), 'hover1': (0, 200, 200), 'accent2': (150, 0, 150), 'hover2': (200, 0, 200),
              'action': (0, 150, 0), 'hover_action': (0, 200, 0), 'warn': (150, 100, 0), 'hover_warn': (200, 150, 0)},
    'light': { 'bg': (240, 240, 240), 'text': (20, 20, 20), 'primary': (180, 180, 180), 'hover': (150, 150, 150),
               'accent1': (0, 120, 120), 'hover1': (0, 160, 160), 'accent2': (120, 0, 120), 'hover2': (160, 0, 160),
               'action': (0, 180, 0), 'hover_action': (0, 220, 0), 'warn': (180, 120, 0), 'hover_warn': (220, 160, 0)}
}

# --- Fonts & Sounds ---
try:
    main_font=pygame.font.Font('assets/font.ttf', 40); label_font=pygame.font.Font('assets/font.ttf', 30); status_font=pygame.font.Font('assets/font.ttf', 24); help_font=pygame.font.Font('assets/font.ttf', 20)
    click_sound = pygame.mixer.Sound('assets/click.wav')
except FileNotFoundError:
    main_font=pygame.font.Font(None, 50); label_font=pygame.font.Font(None, 40); status_font=pygame.font.Font(None, 30); help_font=pygame.font.Font(None, 24)
    click_sound = None

# --- Global State ---
state_manager=StateManager(); animation_generator=None; sort_function_to_run=None
status_message=""; animation_speed=10; sound_enabled=True; is_paused=False; current_theme='dark'; highlighted_line = -1
running = True # Global running flag

# --- UI Elements ---
all_buttons = []
# Menus
ds_button=Button(540,200,200,60,"Data Structures",main_font,('primary','hover')); algo_button=Button(540,280,200,60,"Algorithms",main_font,('primary','hover')); settings_button=Button(540,360,200,60,"Settings",main_font,('primary','hover')); help_button=Button(540,440,200,60,"Help",main_font,('primary','hover'))
tree_button=Button(420,200,200,60,"Trees",main_font,('accent1','hover1')); queue_button=Button(660,200,200,60,"Queue",main_font,('accent1','hover1')); stack_button=Button(420,280,200,60,"Stack",main_font,('accent1','hover1')); ll_button=Button(660,280,200,60,"Linked List",main_font,('accent1','hover1')); heap_button=Button(420,360,200,60,"Heap",main_font,('accent1','hover1')); array_button=Button(660,360,200,60,"Array",main_font,('accent1','hover1')); trie_button = Button(540, 440, 200, 60, "Trie", main_font, ('accent1', 'hover1'))
bst_button=Button(420,300,200,60,"BST",main_font,('accent1','hover1')); rbt_button=Button(660,300,200,60,"Red-Black Tree",main_font,('accent1','hover1'))
sorting_algo_button=Button(420,300,200,60,"Sorting",main_font,('accent2','hover2')); searching_algo_button=Button(660,300,200,60,"Searching",main_font,('accent2','hover2'))
selection_sort_button=Button(540,200,200,60,"Selection Sort",main_font,('accent2','hover2')); bubble_sort_button=Button(540,300,200,60,"Bubble Sort",main_font,('accent2','hover2')); insertion_sort_button=Button(540,400,200,60,"Insertion Sort",main_font,('accent2','hover2'))
back_button=Button(20,20,100,50,"Back",main_font,('warn','hover_warn'))
# Inputs & Ops Buttons
input_box_value=InputBox(150,650,140,50,main_font); input_box_index=InputBox(400,650,140,50,main_font)
insert_button=Button(600,650,150,50,"Insert",main_font,('action','hover_action')); delete_button=Button(770,650,150,50,"Delete",main_font,('warn','hover_warn'));
enqueue_button=Button(260,650,150,50,"Enqueue",main_font,('action','hover_action')); dequeue_button=Button(430,650,150,50,"Dequeue",main_font,('warn','hover_warn'));
push_button=Button(260,650,150,50,"Push",main_font,('action','hover_action')); pop_button=Button(430,650,150,50,"Pop",main_font,('warn','hover_warn'));
insert_head_button=Button(260,650,180,50,"Insert Head",main_font,('action','hover_action')); extract_min_button=Button(430,650,180,50,"Extract Min",main_font,('warn','hover_warn'));
start_button=Button(200,650,150,50,"Start",main_font,('action','hover_action')); reset_button=Button(370,650,150,50,"Reset",main_font,('warn','hover_warn'))
array_search_button = Button(940,650,150,50,"Search",main_font,('accent1','hover1')); binary_search_button = Button(600,650,150,50,"Search",main_font,('action','hover_action')); trie_search_button = Button(770,650,150,50,"Search",main_font,('accent1','hover1'))
# Settings & Controls
theme_button=Button(SCREEN_WIDTH/2-150,250,300,60,"Toggle Theme",main_font,('accent2','hover2')); sound_button=Button(SCREEN_WIDTH/2-150,350,300,60,f"Sound: {'ON' if sound_enabled else 'OFF'}",main_font,('accent2','hover2'))
pause_button=Button(SCREEN_WIDTH-300,20,60,50,"||",main_font,('primary','hover')); step_button=Button(SCREEN_WIDTH-370,20,60,50,">|",main_font,('primary','hover')); speed_down_button=Button(SCREEN_WIDTH-230,20,50,50,"-",main_font,('primary','hover')); speed_up_button=Button(SCREEN_WIDTH-80,20,50,50,"+",main_font,('primary','hover'))
all_buttons.extend([ds_button, algo_button, settings_button, help_button, tree_button, queue_button, stack_button, ll_button, heap_button, array_button, trie_button, bst_button, rbt_button, sorting_algo_button, searching_algo_button, selection_sort_button, bubble_sort_button, insertion_sort_button, back_button, insert_button, delete_button, array_search_button, binary_search_button, trie_search_button, enqueue_button, dequeue_button, push_button, pop_button, insert_head_button, extract_min_button, start_button, reset_button, theme_button, sound_button, pause_button, step_button, speed_down_button, speed_up_button])

# --- Visualizer Instances ---
bst_viz=BSTVisualizer(SCREEN_WIDTH); rbt_viz=RBTreeVisualizer(SCREEN_WIDTH); queue_viz=QueueVisualizer(SCREEN_WIDTH/2-(5*90)/2,SCREEN_HEIGHT/2-40); stack_viz=StackVisualizer(SCREEN_WIDTH/2-60,SCREEN_HEIGHT-150); ll_viz=LinkedListVisualizer(50,SCREEN_HEIGHT/2-25); heap_viz=MinHeapVisualizer(SCREEN_WIDTH); array_viz=ArrayVisualizer(SCREEN_WIDTH/2-(10*80)/2+40,SCREEN_HEIGHT/2-40); trie_viz=TrieVisualizer(SCREEN_WIDTH); sorting_viz=SortingVisualizer(50, 100, SCREEN_WIDTH - 450, SCREEN_HEIGHT - 250); searching_viz=SearchingVisualizer(100,300,SCREEN_WIDTH-200,80)

def update_all_themes():
    for button in all_buttons: button.update_theme(THEMES[current_theme])
    input_box_value.color_inactive = THEMES[current_theme]['primary']; input_box_value.color_active = THEMES[current_theme]['accent1']
    input_box_index.color_inactive = THEMES[current_theme]['primary']; input_box_index.color_active = THEMES[current_theme]['accent1']
def play_click_sound():
    if sound_enabled and click_sound: click_sound.play()
def start_anim(generator_func, *args):
    global animation_generator, status_message, is_paused;
    if animation_generator is None: animation_generator=generator_func(*args); status_message=""; is_paused=False; input_box_value.text=''; input_box_index.text=''
def draw_multiline_text(surface, text, pos, font, color):
    for i, line in enumerate(text.splitlines()): surface.blit(font.render(line.strip(), True, color), (pos[0], pos[1] + i * font.get_height()))
update_all_themes()

# --- Main Loop (Async for Web Compatibility) ---
async def main():
    global running, state_manager, animation_generator, sort_function_to_run, status_message, animation_speed, sound_enabled, is_paused, current_theme, highlighted_line

    while running:
        current_state = state_manager.get_current_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            def handle_button_event(button):
                if button.handle_event(event): play_click_sound(); return True
                return False
            if current_state != "main_menu" and handle_button_event(back_button): state_manager.pop_state(); animation_generator=None; status_message=""; highlighted_line = -1
            if animation_generator:
                if handle_button_event(pause_button): is_paused = not is_paused
                if handle_button_event(step_button) and is_paused:
                    try:
                        result=next(animation_generator)
                        if isinstance(result, dict): status_message = result.get('msg', status_message); highlighted_line = result.get('line', highlighted_line)
                    except StopIteration: animation_generator=None; status_message="Finished!"
            if current_state.endswith("_visualizer"):
                if handle_button_event(speed_down_button): animation_speed=max(5,animation_speed-5)
                if handle_button_event(speed_up_button): animation_speed=min(60,animation_speed+20)

            if current_state == "main_menu":
                if handle_button_event(ds_button): state_manager.push_state("ds_menu")
                if handle_button_event(algo_button): state_manager.push_state("algo_menu")
                if handle_button_event(settings_button): state_manager.push_state("settings_menu")
                if handle_button_event(help_button): state_manager.push_state("help_menu")
            elif current_state == "ds_menu":
                if handle_button_event(tree_button): state_manager.push_state("tree_menu")
                if handle_button_event(queue_button): state_manager.push_state("queue_visualizer")
                if handle_button_event(stack_button): state_manager.push_state("stack_visualizer")
                if handle_button_event(ll_button): state_manager.push_state("ll_visualizer")
                if handle_button_event(heap_button): state_manager.push_state("heap_visualizer")
                if handle_button_event(array_button): state_manager.push_state("array_visualizer"); array_viz.populate_random(7)
                if handle_button_event(trie_button): state_manager.push_state("trie_visualizer")
            elif current_state == "tree_menu":
                if handle_button_event(bst_button): state_manager.push_state("bst_visualizer")
                if handle_button_event(rbt_button): state_manager.push_state("rbt_visualizer")
            elif current_state == "algo_menu":
                if handle_button_event(sorting_algo_button): state_manager.push_state("sorting_menu")
                if handle_button_event(searching_algo_button): state_manager.push_state("binary_search_visualizer"); searching_viz.generate_sorted_array()
            elif current_state == "sorting_menu":
                def select_sort(sort_func): global sort_function_to_run; sort_function_to_run=sort_func; sorting_viz.generate_array(); state_manager.push_state("sorting_visualizer")
                if handle_button_event(selection_sort_button): select_sort(sorting_viz.selection_sort)
                if handle_button_event(bubble_sort_button): select_sort(sorting_viz.bubble_sort)
                if handle_button_event(insertion_sort_button): select_sort(sorting_viz.insertion_sort)
            elif current_state == "settings_menu":
                if handle_button_event(theme_button): current_theme='light' if current_theme=='dark' else 'dark'; update_all_themes()
                if handle_button_event(sound_button): sound_enabled=not sound_enabled; sound_button.text=f"Sound: {'ON' if sound_enabled else 'OFF'}"

            if current_state.endswith("_visualizer"):
                val_from_input=input_box_value.handle_event(event); text_in_val_box=input_box_value.text
                if current_state == "sorting_visualizer":
                    if handle_button_event(start_button): start_anim(sort_function_to_run)
                    if handle_button_event(reset_button): sorting_viz.generate_array(); animation_generator=None; status_message=""; highlighted_line=-1
                elif current_state in ["bst_visualizer", "rbt_visualizer", "heap_visualizer"]:
                    viz = bst_viz if current_state=="bst_visualizer" else rbt_viz if current_state=="rbt_visualizer" else heap_viz
                    if val_from_input and val_from_input.isdigit(): start_anim(viz.insert, int(val_from_input))
                    if handle_button_event(insert_button) and text_in_val_box.isdigit(): start_anim(viz.insert, int(text_in_val_box))
                    if current_state=="heap_visualizer" and handle_button_event(extract_min_button): start_anim(heap_viz.extract_min)
                elif current_state == "binary_search_visualizer":
                    if handle_button_event(binary_search_button) and text_in_val_box.isdigit(): start_anim(searching_viz.binary_search, int(text_in_val_box))
                    if handle_button_event(reset_button): searching_viz.generate_sorted_array(); animation_generator=None; status_message=""
                elif current_state == "array_visualizer":
                    input_box_index.handle_event(event); text_in_idx_box = input_box_index.text
                    if handle_button_event(insert_button) and text_in_val_box.isdigit() and text_in_idx_box.isdigit(): start_anim(array_viz.insert, int(text_in_val_box), int(text_in_idx_box))
                    if handle_button_event(delete_button) and text_in_idx_box.isdigit(): start_anim(array_viz.delete, int(text_in_idx_box))
                    if handle_button_event(array_search_button) and text_in_val_box.isdigit(): start_anim(array_viz.search, int(text_in_val_box))
                elif current_state == "queue_visualizer":
                    if handle_button_event(enqueue_button) and text_in_val_box: start_anim(queue_viz.enqueue, text_in_val_box)
                    if handle_button_event(dequeue_button): start_anim(queue_viz.dequeue)
                elif current_state == "stack_visualizer":
                    if handle_button_event(push_button) and text_in_val_box: start_anim(stack_viz.push, text_in_val_box)
                    if handle_button_event(pop_button): start_anim(stack_viz.pop)
                elif current_state == "ll_visualizer":
                    if handle_button_event(insert_head_button) and text_in_val_box: start_anim(ll_viz.insert_at_beginning, text_in_val_box)
                    if handle_button_event(delete_button) and text_in_val_box: start_anim(ll_viz.delete_value, text_in_val_box)
                elif current_state == "trie_visualizer":
                    if handle_button_event(insert_button) and text_in_val_box: start_anim(trie_viz.insert, text_in_val_box)
                    if handle_button_event(trie_search_button) and text_in_val_box: start_anim(trie_viz.search, text_in_val_box)

        if animation_generator and not is_paused:
            try:
                result = next(animation_generator)
                if isinstance(result, dict): status_message = result.get('msg', status_message); highlighted_line = result.get('line', highlighted_line)
            except StopIteration: animation_generator = None; status_message = "Finished!"

        theme_colors = THEMES[current_theme]
        screen.fill(theme_colors['bg'])
        
        if current_state == "main_menu": ds_button.draw(screen); algo_button.draw(screen); settings_button.draw(screen); help_button.draw(screen)
        elif current_state == "ds_menu": tree_button.draw(screen); queue_button.draw(screen); stack_button.draw(screen); ll_button.draw(screen); heap_button.draw(screen); array_button.draw(screen); trie_button.draw(screen); back_button.draw(screen)
        elif current_state == "tree_menu": bst_button.draw(screen); rbt_button.draw(screen); back_button.draw(screen)
        elif current_state == "algo_menu": sorting_algo_button.draw(screen); searching_algo_button.draw(screen); back_button.draw(screen)
        elif current_state == "sorting_menu": selection_sort_button.draw(screen); bubble_sort_button.draw(screen); insertion_sort_button.draw(screen); back_button.draw(screen)
        elif current_state == "settings_menu": theme_button.draw(screen); sound_button.draw(screen); back_button.draw(screen)
        elif current_state == "help_menu":
            help_text = "Welcome!\n\n- Use menus to select a Data Structure or Algorithm.\n- Use input boxes and buttons at the bottom to operate.\n\nAnimation Controls (Top Right):\n- Pause/Resume, Step Forward, and Speed +/-"
            draw_multiline_text(screen, help_text, (50, 150), help_font, theme_colors['text']); back_button.draw(screen)
        elif current_state == "bst_visualizer": bst_viz.draw(screen, main_font); input_box_value.draw(screen); insert_button.draw(screen); back_button.draw(screen)
        elif current_state == "rbt_visualizer": rbt_viz.draw(screen); input_box_value.draw(screen); insert_button.draw(screen); back_button.draw(screen)
        elif current_state == "queue_visualizer": queue_viz.draw(screen); input_box_value.draw(screen); enqueue_button.draw(screen); dequeue_button.draw(screen); back_button.draw(screen)
        elif current_state == "stack_visualizer": stack_viz.draw(screen); input_box_value.draw(screen); push_button.draw(screen); pop_button.draw(screen); back_button.draw(screen)
        elif current_state == "ll_visualizer": ll_viz.draw(screen); input_box_value.draw(screen); insert_head_button.draw(screen); delete_button.draw(screen); back_button.draw(screen)
        elif current_state == "heap_visualizer": heap_viz.draw(screen); input_box_value.draw(screen); insert_button.draw(screen); extract_min_button.draw(screen); back_button.draw(screen)
        elif current_state == "array_visualizer":
            array_viz.draw(screen); input_box_value.draw(screen); input_box_index.draw(screen); insert_button.draw(screen); delete_button.draw(screen); array_search_button.draw(screen); back_button.draw(screen)
            val_label=label_font.render("Value",True,theme_colors['text']); screen.blit(val_label, (150, 620)); idx_label=label_font.render("Index",True,theme_colors['text']); screen.blit(idx_label,(400,620))
        elif current_state == "sorting_visualizer":
            sorting_viz.draw(screen); start_button.draw(screen); reset_button.draw(screen); back_button.draw(screen)
            code_panel = CodePanel(SCREEN_WIDTH - 380, 100, 360, SCREEN_HEIGHT - 250, sorting_viz.PSEUDOCODE[sort_function_to_run.__name__], help_font, theme_colors)
            code_panel.draw(screen, highlighted_line)
        elif current_state == "binary_search_visualizer":
            searching_viz.draw(screen); input_box_value.draw(screen); binary_search_button.draw(screen); reset_button.draw(screen); back_button.draw(screen)
            val_label=label_font.render("Target",True,theme_colors['text']); screen.blit(val_label,(150,620))
        elif current_state == "trie_visualizer":
            trie_viz.draw(screen); input_box_value.draw(screen); insert_button.draw(screen); trie_search_button.draw(screen); back_button.draw(screen)
            val_label=label_font.render("Word",True,theme_colors['text']); screen.blit(val_label,(150,620))

        if animation_generator: pause_button.text=">" if is_paused else "||"; pause_button.draw(screen); step_button.draw(screen)
        if current_state.endswith("_visualizer"):
            speed_down_button.draw(screen); speed_up_button.draw(screen)
            speed_text=label_font.render(f"Speed: {animation_speed}",True,theme_colors['text']); screen.blit(speed_text,(SCREEN_WIDTH-195,30))
            if status_message: status_surf=status_font.render(status_message,True,theme_colors['text']); screen.blit(status_surf,status_surf.get_rect(center=(SCREEN_WIDTH/2,40)))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

# Run the async main loop
asyncio.run(main())