import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.init()
# Initialize audio if available; fall back gracefully when mixer isn't built
AUDIO_ENABLED = False
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    AUDIO_ENABLED = True
except Exception:
    AUDIO_ENABLED = False

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Thanksgiving Address - Adam Bizios')

#define font
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)
font_message = pygame.font.SysFont('Arial', 24)
font_message_small = pygame.font.SysFont('Arial', 20) 

#define game variables
tile_size = 50
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0
collectible_collected = False
show_message = False
message_timer = 0
message_duration = 5000  # 5 seconds
paused = False
show_controls_menu = False
music_muted = False
show_intro = False
show_big_coin_anim = False
big_coin_timer = 0
big_coin_duration = 2000  # 2 seconds for animation
show_opening_message = False
opening_message_done = False

# Final completion animation variables
show_final_animation = False
final_animation_timer = 0
final_animation_duration = 4000  # 4 seconds for final animation
final_collectibles = []  # Will store all collectible positions for animation
show_final_restart = False
current_collectible_level = None
current_collectible_data = None

#define colours
white = (255, 255, 255)
blue = (0, 0, 255)
gold = (255, 215, 0)
dark_green = (0, 100, 0)
light_blue = (173, 216, 230)
purple = (128, 0, 128)
orange = (255, 165, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Level-specific collectible data
level_collectibles = {
    1: {
        'name': 'Unity Symbol',
        'color': gold,
        'message': "We will wrap our minds as one and thank/honor\nAll the People.\nStill we are working together for peace, strength, and good minds here on earth.\nSo let it be in our minds.",
        'symbol': '🪶'
    },
    2: {
        'name': 'Heart of the Earth',
        'color': dark_green,
        'message': "We will wrap our minds as one and thank/honor\nOur Mother the Earth.\nThat still she goes along giving up her powers that we need\nfor us to live a good life and for it to be peaceful where we are.\nSo let it be in our minds.",
        'symbol': '🌎'
    },
    3: {
        'name': 'Water Drop Spirit',
        'color': light_blue,
        'message': "We will wrap our minds as one and thank/honor\nThe Waters.\nThat still they wipe away what is bad on the earth.\nAnd also, they quench the thirst of the plants, animals, and people.\nSo let it be in our minds.",
        'symbol': '💧'
    },
    4: {
        'name': 'Three Sisters Seed',
        'color': dark_green,
        'message': "We will wrap our minds as one and thank/honor\nEverything Natural Growing Under and On the Earth:\nthe roots, grasses, flowers, medicines, fruits, sustenance foods, and the trees & bushes.\nSo let it be in our minds.",
        'symbol': '🌿'
    },
    5: {
        'name': 'Sacred Feather',
        'color': purple,
        'message': "We will wrap our minds as one and thank/honor\nAll the Life Running About on Earth and Flying in the Sky:\nthe bugs, animals, and birds.\nStill they are doing their responsibilities; they help us, carry songs to wake our minds,\nand tell us when danger is coming.\nSo let it be in our minds.",
        'symbol': '🐾'
    },
    6: {
        'name': 'Star Crystal',
        'color': orange,
        'message': "We will wrap our minds as one and thank/honor\nEverything Working Together in the Sky:\nthe Four Winds, Our Grandfathers the Thunders,\nOur Elder Brother the Sun, Our Grandmother the Moon, and the Stars.\nStill they bring new winds, they make new waters, they protect us,\nand make it bright for us.\nSo let it be in our minds.",
        'symbol': '☀️'
    },
    7: {
        'name': 'Sacred Flame',
        'color': red,
        'message': "We will wrap our minds as one and thank/honor\nThe Creator (He That Finished Our Bodies).\nWe are grateful for all he has put together and made useful.\nWe are happy that we are still here.\nSo let it be in our minds.",
        'symbol': '✨'
    }
}

final_message = "And now I did all I was able to do.\nIf I have forgotten anything, you all can continue it on further.\nThat's all the words, and that's all."
opening_message = (
    "I will open the business and raise the words of thanksgiving.\n"
    "We will wrap our minds as one and thank/honor\n"
    "All the Great Natural Powers.\n"
    "So let it be in our minds."
)

#load images
sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/sky.png')
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')

# retro pixel text and button helpers
def render_pixel_text(text, color, scale=3):
	base_font = pygame.font.SysFont('Courier New', 12, bold=True)
	text_surf = base_font.render(text, False, color)
	w, h = text_surf.get_width(), text_surf.get_height()
	return pygame.transform.scale(text_surf, (w * scale, h * scale))

def make_pixel_button(label_text, size=(220, 80)):
	btn_w, btn_h = size
	# shadow
	shadow = pygame.Surface(size, pygame.SRCALPHA)
	shadow.fill((0, 0, 0, 120))
	# button face
	img = pygame.Surface(size, pygame.SRCALPHA)
	img.fill((240, 240, 240))
	pygame.draw.rect(img, (200, 200, 200), (0, 0, btn_w, btn_h))
	pygame.draw.rect(img, blue, (0, 0, btn_w, btn_h), 6)
	# label (8-bit style)
	label = render_pixel_text(label_text.upper(), (25, 60, 180), scale=3)
	label_rect = label.get_rect(center=(btn_w // 2, btn_h // 2))
	# compose shadow + button
	button_with_shadow = pygame.Surface((btn_w + 8, btn_h + 8), pygame.SRCALPHA)
	button_with_shadow.blit(shadow, (8, 8))
	button_with_shadow.blit(img, (0, 0))
	button_with_shadow.blit(label, label_rect)
	return button_with_shadow

# create custom retro-styled button images
start_pixel_img = make_pixel_button('Start')
exit_pixel_img = make_pixel_button('Exit')
controls_img = make_pixel_button('Controls')
back_img = make_pixel_button('Back')
resume_pixel_img = make_pixel_button('Resume')
skip_img = make_pixel_button('Skip', size=(120, 48))
restart_pixel_img = make_pixel_button('Restart')
mute_img = make_pixel_button('Mute', size=(160, 60))
unmute_img = make_pixel_button('Unmute', size=(160, 60))
continue_img = make_pixel_button('Continue', size=(180, 60))

#load sounds (only if audio is available)
def play_sound(sound):
    if sound is not None and AUDIO_ENABLED:
        try:
            sound.play()
        except Exception:
            pass

coin_fx = None
jump_fx = None
game_over_fx = None
if AUDIO_ENABLED:
    try:
        pygame.mixer.music.load('img/music.wav')
        pygame.mixer.music.play(-1, 0.0, 5000)
    except Exception:
        pass
    try:
        coin_fx = pygame.mixer.Sound('img/coin.wav')
        coin_fx.set_volume(0.5)
    except Exception:
        coin_fx = None
    try:
        jump_fx = pygame.mixer.Sound('img/jump.wav')
        jump_fx.set_volume(0.5)
    except Exception:
        jump_fx = None
    try:
        game_over_fx = pygame.mixer.Sound('img/game_over.wav')
        game_over_fx.set_volume(0.5)
    except Exception:
        game_over_fx = None


def draw_4winds_orb_animation(surface, size, timer):
	"""Draw the 4winds orb for the big coin animation"""
	center_x, center_y = size // 2, size // 2
	
	# Outer ring - pale silver/blue-white (Moon & Winds)
	outer_radius = size // 2 - 20
	pygame.draw.circle(surface, (200, 220, 255), (center_x, center_y), outer_radius)
	
	# Center - bright gold (Sun)
	inner_radius = outer_radius - 20
	pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), inner_radius)
	
	# Add tiny white stars orbiting
	star_radius = outer_radius - 10
	for i in range(4):
		angle = (timer * 0.1 + i * 90) % 360
		star_x = center_x + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).x)
		star_y = center_y + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).y)
		pygame.draw.circle(surface, white, (star_x, star_y), 4)
	
	# Add occasional purple flashes (Thunderers)
	if int(timer * 0.01) % 3 == 0:
		flash_radius = inner_radius + 5
		pygame.draw.circle(surface, (150, 50, 200), (center_x, center_y), flash_radius, 4)


def draw_4winds_orb_final(surface, size, timer):
	"""Draw the 4winds orb for the final animation"""
	center_x, center_y = size // 2, size // 2
	
	# Outer ring - pale silver/blue-white (Moon & Winds)
	outer_radius = size // 2 - 5
	pygame.draw.circle(surface, (200, 220, 255), (center_x, center_y), outer_radius)
	
	# Center - bright gold (Sun)
	inner_radius = outer_radius - 5
	pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), inner_radius)
	
	# Add tiny white stars orbiting
	star_radius = outer_radius - 2
	for i in range(4):
		angle = (timer * 0.1 + i * 90) % 360
		star_x = center_x + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).x)
		star_y = center_y + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).y)
		pygame.draw.circle(surface, white, (star_x, star_y), 1)
	
	# Add occasional purple flashes (Thunderers)
	if int(timer * 0.01) % 3 == 0:
		flash_radius = inner_radius + 1
		pygame.draw.circle(surface, (150, 50, 200), (center_x, center_y), flash_radius, 1)


def draw_final_animation():
    """Draw the final animation: seamless black screen with circles coming together"""
    global final_animation_timer, show_final_animation, show_final_restart

    progress = min(final_animation_timer / final_animation_duration, 1.0)
    screen_center_x, screen_center_y = screen_width // 2, screen_height // 2

    # Always draw black background first
    black_surface = pygame.Surface((screen_width, screen_height))
    black_surface.fill((0, 0, 0))
    screen.blit(black_surface, (0, 0))

    # Phase 1: Brief pause on black screen (first 20% of animation)
    if progress < 0.2:
        return

    # Phase 2: Circles come together (remaining 80% of animation)
    circle_progress = (progress - 0.2) / 0.8

    # Start circles far apart, come together
    start_radius = 300
    end_radius = 80
    circle_radius = int(start_radius - (start_radius - end_radius) * circle_progress)

    # Draw all 7 collectibles in correct order
    sprite_files = {
        1: 'unity.png',
        2: 'earth.png',
        3: 'water.png',
        4: 'threesisters.png',
        5: 'feather.png',
        6: '4winds_orb',  # Special case - will be drawn as custom orb
        7: 'spirit.png'
    }

    for i, (level_num, collectible_data) in enumerate(level_collectibles.items()):
        # Calculate position on circle - maintain correct order
        angle = i * (360 / 7)  # Fixed positions, no rotation
        base_x = screen_center_x + int(circle_radius * pygame.math.Vector2(1, 0).rotate(angle).x)
        base_y = screen_center_y + int(circle_radius * pygame.math.Vector2(1, 0).rotate(angle).y)

        # Add gentle pulsing effect
        pulse = 1 + 0.2 * abs(pygame.math.Vector2(1, 0).rotate(final_animation_timer * 0.05).x)
        size = int(50 * pulse)

        # Draw glowing circle
        glow_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*collectible_data['color'], 180), (size, size), size)

        # Draw main circle
        main_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(main_surface, collectible_data['color'], (size // 2, size // 2), size // 2 - 5)
        pygame.draw.circle(main_surface, white, (size // 2, size // 2), size // 2 - 5, 3)

        # Draw custom sprite or symbol
        try:
            if level_num in sprite_files:
                if sprite_files[level_num] == '4winds_orb':
                    # Special case: Draw custom glowing orb for 4winds
                    draw_4winds_orb_final(main_surface, size, final_animation_timer)
                else:
                    sprite_img = pygame.image.load(f'img/{sprite_files[level_num]}').convert_alpha()
                    sprite_img = pygame.transform.scale(sprite_img, (size - 10, size - 10))
                    sprite_rect = sprite_img.get_rect(center=(size // 2, size // 2))
                    main_surface.blit(sprite_img, sprite_rect)
            else:
                # Fallback to symbol if level not found
                symbol_font = pygame.font.SysFont('Arial', size // 2)
                symbol_text = symbol_font.render(collectible_data['symbol'], True, white)
                symbol_rect = symbol_text.get_rect(center=(size // 2, size // 2))
                main_surface.blit(symbol_text, symbol_rect)
        except:
            # Fallback to symbol if sprite loading fails
            symbol_font = pygame.font.SysFont('Arial', size // 2)
            symbol_text = symbol_font.render(collectible_data['symbol'], True, white)
            symbol_rect = symbol_text.get_rect(center=(size // 2, size // 2))
            main_surface.blit(symbol_text, symbol_rect)

        # Blit to screen
        glow_rect = glow_surface.get_rect(center=(base_x, base_y))
        main_rect = main_surface.get_rect(center=(base_x, base_y))
        screen.blit(glow_surface, glow_rect)
        screen.blit(main_surface, main_rect)

    # NOTE: Phase 3 text REMOVED — we go straight to the final card afterwards.

    # Complete animation
    if progress >= 1.0:
        show_final_animation = False
        show_final_restart = True


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


def draw_multiline_text(text, font, text_col, x, y, line_height=30):
	lines = text.split('\n')
	for i, line in enumerate(lines):
		draw_text(line, font, text_col, x, y + i * line_height)


def draw_big_coin_animation():
	"""Draw the big coin animation for the current collectible."""
	global big_coin_timer, show_big_coin_anim, show_message, message_timer
	
	# Calculate animation progress (0 to 1)
	progress = min(big_coin_timer / big_coin_duration, 1.0)
	
	# Create big coin surface
	coin_size = int(400 + 200 * progress)  # Grows from 400 to 600
	coin_surface = pygame.Surface((coin_size, coin_size), pygame.SRCALPHA)
	
	# Determine color from current collectible; fallback to gold
	base_color = (current_collectible_data['color'] if current_collectible_data else gold)
	pygame.draw.circle(coin_surface, base_color, (coin_size // 2, coin_size // 2), coin_size // 2)
	pygame.draw.circle(coin_surface, (200, 150, 0), (coin_size // 2, coin_size // 2), coin_size // 2, 8)
	
	# Add center image/symbol
	try:
		# Map level numbers to sprite filenames
		sprite_files = {
			1: 'unity.png',
			2: 'earth.png', 
			3: 'water.png',
			4: 'threesisters.png',
			5: 'feather.png',
			6: '4winds_orb',  # Special case - will be drawn as custom orb
			7: 'spirit.png'
		}
		
		if current_collectible_level in sprite_files:
			if sprite_files[current_collectible_level] == '4winds_orb':
				# Special case: Draw custom glowing orb for 4winds
				draw_4winds_orb_animation(coin_surface, coin_size, big_coin_timer)
			else:
				sprite_img = pygame.image.load(f'img/{sprite_files[current_collectible_level]}').convert_alpha()
				img_size = int(coin_size * 0.6)
				sprite_img = pygame.transform.scale(sprite_img, (img_size, img_size))
				sprite_rect = sprite_img.get_rect(center=(coin_size // 2, coin_size // 2))
				coin_surface.blit(sprite_img, sprite_rect)
		else:
			# Fallback to symbol if level not found
			symbol = current_collectible_data['symbol'] if current_collectible_data else '★'
			symbol_font = pygame.font.SysFont('Arial', max(24, coin_size // 3))
			symbol_text = symbol_font.render(symbol, True, white)
			symbol_rect = symbol_text.get_rect(center=(coin_size // 2, coin_size // 2))
			coin_surface.blit(symbol_text, symbol_rect)
	except Exception:
		# Fallback to star if anything fails
		symbol_font = pygame.font.SysFont('Arial', max(24, coin_size // 3))
		symbol_text = symbol_font.render('★', True, white)
		symbol_rect = symbol_text.get_rect(center=(coin_size // 2, coin_size // 2))
		coin_surface.blit(symbol_text, symbol_rect)
	
	# Apply flip effect in second half
	if progress > 0.5:
		flip_progress = (progress - 0.5) * 2
		coin_surface = pygame.transform.flip(coin_surface, True, False)
		coin_surface.set_alpha(int(255 * (1 - flip_progress * 0.3)))
	
	# Center the coin on screen
	coin_rect = coin_surface.get_rect(center=(screen_width // 2, screen_height // 2))
	screen.blit(coin_surface, coin_rect)
	
	# When animation finishes, show message
	if progress >= 1.0:
		show_big_coin_anim = False
		show_message = True
		message_timer = pygame.time.get_ticks()

def draw_message_box(message, collectible_name, symbol):
    # Draw semi-transparent background
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Draw message box
    box_width = screen_width - 100
    box_height = 300
    box_x = 50
    box_y = (screen_height - box_height) // 2

    pygame.draw.rect(screen, white, (box_x, box_y, box_width, box_height))
    pygame.draw.rect(screen, blue, (box_x, box_y, box_width, box_height), 5)

    # Title
    safe_symbol = symbol if symbol.isascii() else ""  # keep only ASCII characters
    title_text = f"{safe_symbol} {collectible_name} Collected!".strip()
    draw_text(title_text, font_score, blue, box_x + 20, box_y + 20)

    # Choose smaller font when text is long
    lines = message.split('\n')
    use_small = (len(lines) > 5) or (len(message) > 220)
    msg_font = font_message_small if use_small else font_message
    line_h = 26 if use_small else 30

    # Message
    draw_multiline_text(message, msg_font, dark_green, box_x + 20, box_y + 60, line_height=line_h)

    # Instruction
    draw_text("Press SPACE to continue...", msg_font, blue, box_x + 20, box_y + 250)


def draw_controls_overlay():
	# Dim background
	overlay = pygame.Surface((screen_width, screen_height))
	overlay.set_alpha(180)
	overlay.fill((0, 0, 0))
	screen.blit(overlay, (0, 0))

	box_width = screen_width - 200
	box_height = 400
	box_x = 100
	box_y = (screen_height - box_height) // 2
	pygame.draw.rect(screen, white, (box_x, box_y, box_width, box_height))
	pygame.draw.rect(screen, blue, (box_x, box_y, box_width, box_height), 5)

	draw_text('Controls', font, blue, box_x + 30, box_y + 20)
	info_y = box_y + 110
	lines = [
		'Arrows Left/Right: Move',
		'Space: Jump (press twice for Double Jump)',
		'Space (when a message shows): Dismiss message',
		'ESC: Pause, view Controls, Resume or Exit'
	]
	for i, line in enumerate(lines):
		draw_text(line, font_message, dark_green, box_x + 30, info_y + i * 30)

	return pygame.Rect(box_x, box_y, box_width, box_height)


#function to reset level
def reset_level(level):
	global collectible_collected, show_message, message_timer
	collectible_collected = False
	show_message = False
	message_timer = 0
	
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()
	collectible_group.empty()

	#load in level data and create world
	if path.exists(f'level{level}_data'):
		pickle_in = open(f'level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		screen.blit(self.image, self.rect)

		return action


class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0
		dy = 0
		walk_cooldown = 5
		col_thresh = 20

		if game_over == 0:
			#get keypresses
			key = pygame.key.get_pressed()
			# allow up to two jumps (double-jump)
			if key[pygame.K_SPACE] and self.jumped == False and self.jumps_remaining > 0:
				play_sound(jump_fx)
				self.vel_y = -18
				self.jumped = True
				self.jumps_remaining -= 1
			if key[pygame.K_SPACE] == False:
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5
				self.counter += 1
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
				self.counter = 0
				self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			#handle animation
			if self.counter > walk_cooldown:
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right):
					self.index = 0
				if self.direction == 1:
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]

			#add gravity
			self.vel_y += 1
			if self.vel_y > 10:
				self.vel_y = 10
			dy += self.vel_y

			#check for collision
			self.in_air = True
			for tile in world.tile_list:
				#check for collision in x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#check for collision in y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below the ground i.e. jumping
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					#check if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False
						# reset jumps when grounded
						self.jumps_remaining = self.max_jumps

			#check for collision with enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1
				play_sound(game_over_fx)

			#check for collision with lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				play_sound(game_over_fx)

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				# Only allow exit if collectible has been collected
				if collectible_collected:
					game_over = 1
				else:
					# Show message that collectible is needed
					pass

			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
						# reset jumps when standing on a moving platform
						self.jumps_remaining = self.max_jumps
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction

			#update player coordinates
			self.rect.x += dx
			self.rect.y += dy

		elif game_over == -1:
			self.image = self.dead_image
			draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200:
				self.rect.y -= 5

		#draw player onto screen
		screen.blit(self.image, self.rect)

		return game_over

	def reset(self, x, y):
		self.images_right = []
		self.images_left = []
		self.index = 0
		self.counter = 0
		for num in range(1, 5):
			img_right = pygame.image.load(f'img/guy{num}.png')
			img_right = pygame.transform.scale(img_right, (40, 80))
			img_left = pygame.transform.flip(img_right, True, False)
			self.images_right.append(img_right)
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('img/ghost.png')
		self.image = self.images_right[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.width = self.image.get_width()
		self.height = self.image.get_height()
		self.vel_y = 0
		self.jumped = False
		self.direction = 0
		self.in_air = True
		# double-jump settings
		self.max_jumps = 2
		self.jumps_remaining = self.max_jumps


class World():
	def __init__(self, data):
		self.tile_list = []

		#load images
		dirt_img = pygame.image.load('img/dirt.png')
		grass_img = pygame.image.load('img/grass.png')

		row_count = 0
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 2:
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				if tile == 9:  # New tile type for level collectibles
					collectible = LevelCollectible(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2), level)
					collectible_group.add(collectible)
				col_count += 1
			row_count += 1

	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # load and scale blob image (big blob)
        raw = pygame.image.load('img/blob.png').convert_alpha()
        BIG_BLOB = int(tile_size * 1.5)  # tweak 1.5–2.0 if you want larger
        self.base_image = pygame.transform.scale(raw, (BIG_BLOB, BIG_BLOB))

        # starting direction and first image
        self.move_direction = 1
        self.image = self._image_for_dir(self.move_direction)

        # position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # LIFT ENEMY A BIT so it sits on platforms instead of looking sunk
        self.rect.y -= 8  # <- change this value if you want more/less lift

        self.move_counter = 0

    def _image_for_dir(self, direction):
        # Flip horizontally based on direction; swap > 0 / < 0 to invert facing
        return pygame.transform.flip(self.base_image, direction > 0, False)

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1
            self.image = self._image_for_dir(self.move_direction)


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/platform.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y

	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


class LevelCollectible(pygame.sprite.Sprite):
	def __init__(self, x, y, level_num):
		pygame.sprite.Sprite.__init__(self)
		self.level_num = level_num
		self.collectible_data = level_collectibles[level_num]
		
		# Create a glowing circle for all collectibles
		self.size = tile_size
		self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
		
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		
		# Animation variables
		self.glow_timer = 0
		self.glow_speed = 0.1
		
	def update(self):
		self.glow_timer += self.glow_speed
		
	def draw(self):
		# Draw glowing effect for all levels
		glow_size = int(tile_size + 10 * abs(pygame.math.Vector2(1, 0).rotate(self.glow_timer * 50).x))
		
		# Create glow surface
		glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
		pygame.draw.circle(glow_surface, (*self.collectible_data['color'], 100), 
						  (glow_size, glow_size), glow_size)
		
		# Create circle background for the image
		circle_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
		pygame.draw.circle(circle_surface, self.collectible_data['color'], 
						  (tile_size // 2, tile_size // 2), tile_size // 2 - 5)
		pygame.draw.circle(circle_surface, white, 
						  (tile_size // 2, tile_size // 2), tile_size // 2 - 5, 3)
		
		# Map level numbers to sprite filenames
		sprite_files = {
			1: 'unity.png',
			2: 'earth.png', 
			3: 'water.png',
			4: 'threesisters.png',
			5: 'feather.png',
			6: '4winds_orb',  # Special case - will be drawn as custom orb
			7: 'spirit.png'
		}
		
		# Draw custom sprite for each level or fallback to symbol
		try:
			if self.level_num in sprite_files:
				if sprite_files[self.level_num] == '4winds_orb':
					# Special case: Draw custom glowing orb for 4winds
					self.draw_4winds_orb(circle_surface, tile_size)
				else:
					sprite_img = pygame.image.load(f'img/{sprite_files[self.level_num]}').convert_alpha()
					sprite_img = pygame.transform.scale(sprite_img, (tile_size - 10, tile_size - 10))
					sprite_rect = sprite_img.get_rect(center=(tile_size // 2, tile_size // 2))
					circle_surface.blit(sprite_img, sprite_rect)
			else:
				# Fallback to symbol if level not found
				symbol_font = pygame.font.SysFont('Arial', tile_size // 2)
				symbol_text = symbol_font.render(self.collectible_data['symbol'], True, white)
				symbol_rect = symbol_text.get_rect(center=(tile_size // 2, tile_size // 2))
				circle_surface.blit(symbol_text, symbol_rect)
		except:
			# Fallback to symbol if sprite loading fails
			symbol_font = pygame.font.SysFont('Arial', tile_size // 2)
			symbol_text = symbol_font.render(self.collectible_data['symbol'], True, white)
			symbol_rect = symbol_text.get_rect(center=(tile_size // 2, tile_size // 2))
			circle_surface.blit(symbol_text, symbol_rect)
		
		# Blit glow behind main collectible
		glow_rect = glow_surface.get_rect(center=self.rect.center)
		screen.blit(glow_surface, glow_rect)
		screen.blit(circle_surface, self.rect)
	
	def draw_4winds_orb(self, surface, size):
		"""Draw a custom glowing orb for the 4winds collectible"""
		center_x, center_y = size // 2, size // 2
		
		# Outer ring - pale silver/blue-white (Moon & Winds)
		outer_radius = size // 2 - 8
		pygame.draw.circle(surface, (200, 220, 255), (center_x, center_y), outer_radius)
		
		# Center - bright gold (Sun)
		inner_radius = outer_radius - 8
		pygame.draw.circle(surface, (255, 215, 0), (center_x, center_y), inner_radius)
		
		# Add tiny white stars orbiting
		star_radius = outer_radius - 4
		for i in range(4):
			angle = (self.glow_timer * 30 + i * 90) % 360
			star_x = center_x + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).x)
			star_y = center_y + int(star_radius * pygame.math.Vector2(1, 0).rotate(angle).y)
			pygame.draw.circle(surface, white, (star_x, star_y), 2)
		
		# Add occasional purple flashes (Thunderers)
		if int(self.glow_timer * 10) % 3 == 0:
			flash_radius = inner_radius + 2
			pygame.draw.circle(surface, (150, 50, 200), (center_x, center_y), flash_radius, 2)


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()

#create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'level{level}_data'):
	pickle_in = open(f'level{level}_data', 'rb')
	world_data = pickle.load(pickle_in)
world = World(world_data)


#create buttons (menu buttons)
menu_start_button = Button(0, 0, start_pixel_img)
menu_exit_button = Button(0, 0, exit_pixel_img)
menu_controls_button = Button(0, 0, controls_img)
menu_back_button = Button(0, 0, back_img)

# gameplay/pause HUD buttons
restart_button = Button(0, 0, restart_pixel_img)
resume_button = Button(0, 0, resume_pixel_img)
pause_exit_button = Button(0, 0, exit_pixel_img)
mute_button = Button(0, 0, mute_img)
skip_button = Button(screen_width - 20 - skip_img.get_width(), 10, skip_img)
continue_button = Button(0, 0, continue_img)


run = True
while run:

	clock.tick(fps)

	screen.blit(bg_img, (0, 0))
	# Position sun in top-right corner so only quarter is visible
	screen.blit(sun_img, (screen_width - sun_img.get_width() // 2, -sun_img.get_height() // 2))

	if main_menu == True:
		# draw title
		title_text = render_pixel_text('THANKSGIVING CREATIVE PROJECT\n        By: Adam Bizios', (25, 60, 180), scale=4)
		title_rect = title_text.get_rect(center=(screen_width // 2, 200))
		screen.blit(title_text, title_rect)
		# set menu layout (centered vertical stack)
		center_x = screen_width // 2
		center_y = screen_height // 2 - 40
		menu_start_button.rect.center = (center_x, center_y - 20)
		menu_controls_button.rect.center = (center_x, center_y + 60)
		menu_exit_button.rect.center = (center_x, center_y + 140)
		# menu background
		if menu_exit_button.draw():
			run = False
		if menu_start_button.draw():
			show_intro = True
			main_menu = False
		if menu_controls_button.draw():
			show_controls_menu = True
		# controls overlay inside main menu
		if show_controls_menu:
			draw_controls_overlay()
			menu_back_button.rect.center = (center_x, center_y + 200)
			if menu_back_button.draw():
				show_controls_menu = False
	elif show_intro:
		# intro message screen
		overlay = pygame.Surface((screen_width, screen_height))
		overlay.set_alpha(200)
		overlay.fill((0, 0, 0))
		screen.blit(overlay, (0, 0))
		box_width = screen_width - 200
		box_height = 300
		box_x = 100
		box_y = (screen_height - box_height) // 2
		pygame.draw.rect(screen, white, (box_x, box_y, box_width, box_height))
		pygame.draw.rect(screen, blue, (box_x, box_y, box_width, box_height), 5)
		draw_text('Here is my Thanksgiving creative project,', font_message, dark_green, box_x + 30, box_y + 40)
		draw_text('I coded it on Python, hope you enjoy!', font_message, dark_green, box_x + 30, box_y + 70)
		continue_button.rect.center = (box_x + box_width // 2, box_y + box_height - 60)
		if continue_button.draw():
			show_intro = False
			show_opening_message = True

	elif show_opening_message:
    # dim background
		overlay = pygame.Surface((screen_width, screen_height))
		overlay.set_alpha(200)
		overlay.fill((0, 0, 0))
		screen.blit(overlay, (0, 0))

    # reuse your standard message box look
		draw_message_box(
			opening_message,
			"Opening the Words of Thanksgiving",
			""  # empty symbol so no little blue box shows
		)

		# wait for SPACE to continue (consume events just for this screen)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				show_opening_message = False  # proceed into the level

	else:
		world.draw()

		if paused:
			# Pause overlay content
			box_rect = draw_controls_overlay()
			# Arrange pause buttons neatly inside overlay
			row_y = box_rect.bottom - 90
			resume_button.rect.center = (box_rect.centerx - 180, row_y)
			pause_exit_button.rect.center = (box_rect.centerx + 180, row_y)
			# mute/unmute button state + position
			mute_button.image = unmute_img if music_muted else mute_img
			mute_button.rect.center = (box_rect.centerx, row_y)
			if resume_button.draw():
				paused = False
			if pause_exit_button.draw():
				run = False
			if mute_button.draw() and AUDIO_ENABLED:
				music_muted = not music_muted
				try:
					pygame.mixer.music.set_volume(0.0 if music_muted else 0.5)
				except Exception:
					pass
		elif game_over == 0:
			blob_group.update()
			platform_group.update()
			collectible_group.update()
			
			#update score
			#check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True):
				score += 1
				play_sound(coin_fx)
			
			#check if level collectible has been collected
			if pygame.sprite.spritecollide(player, collectible_group, True):
				collectible_collected = True
				play_sound(coin_fx)
				# Start big coin animation for any level
				current_collectible_level = level
				current_collectible_data = level_collectibles[level]
				show_big_coin_anim = True
				big_coin_timer = 0
			
			draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)
			# show level progress
			draw_text(f'Level {level}/{max_levels}', font_score, white, screen_width // 2 - 60, 10)
			
			# (removed top-right Find text to keep HUD clean)

			# draw Skip Level button (HUD)
			if skip_button.draw():
				game_over = 1
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)
		
		# Draw collectibles with custom draw method
		for collectible in collectible_group:
			collectible.draw()

		game_over = player.update(game_over)

		# Show big coin animation for level 1 collectible
		if show_big_coin_anim:
			big_coin_timer += clock.get_time()
			draw_big_coin_animation()

		# Show final animation if level 7 is completed
		if show_final_animation:
			final_animation_timer += clock.get_time()
			draw_final_animation()
		elif show_final_restart and not show_final_animation:
			# Animation completed, show final message
			pass

		# Show message if collectible was just collected
		if show_message:
			current_time = pygame.time.get_ticks()
			if current_time - message_timer < message_duration and current_collectible_level in level_collectibles:
				collectible_data = level_collectibles[current_collectible_level]
				draw_message_box(collectible_data['message'], collectible_data['name'], collectible_data['symbol'])
			else:
				show_message = False
		
		# Show final completion message with buttons (persistent until user chooses)
		if show_final_restart:
			# Draw black background
			black_surface = pygame.Surface((screen_width, screen_height))
			black_surface.fill((0, 0, 0))
			screen.blit(black_surface, (0, 0))
			
			# Draw final message
			draw_message_box(final_message, "Journey Complete", "🌟")
			
			# Position buttons side by side with more spacing
			button_y = screen_height - 150
			restart_button.rect.center = (screen_width // 2 - 120, button_y)
			pause_exit_button.rect.center = (screen_width // 2 + 120, button_y)
			
			if restart_button.draw():
				level = 1
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0
				show_final_restart = False
			elif pause_exit_button.draw():
				run = False

		#if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			#reset game and go to next level
			level += 1
			if level <= max_levels:
				#reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				# Trigger final animation for level 7 completion
				if not show_final_animation and not show_final_restart:
					show_final_animation = True
					final_animation_timer = 0
					game_over = 0  # Reset game_over so we can show animation
					score = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		# Handle space key for dismissing messages
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE and main_menu == False:
				paused = not paused
			if event.key == pygame.K_SPACE and show_message:
				show_message = False

	pygame.display.update()

pygame.quit()
