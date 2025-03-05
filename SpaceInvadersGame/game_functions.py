import sys
import pygame
from time import sleep

from alien import Alien
from bullet import Bullet

#key events

def check_events(settings, screen, stats, scoreboard, ship, bullets, aliens, play_button):
    """Respond to keyevents"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.KEYDOWN:
            key_down(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.KEYUP:
            key_up(event, settings, screen, ship, bullets)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, scoreboard, ship, bullets, aliens, play_button, mouse_x, mouse_y)

def key_down(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # move the ship right
        ship.right = True

    elif event.key == pygame.K_LEFT:
        # move the ship left
        ship.left = True
        
    elif event.key == pygame.K_SPACE:
        # fires a bullet
        fire_bullet(settings, screen, ship, bullets)
    
    elif event.key == pygame.K_q:
        #quit on q
        sys.exit()

def key_up(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        # move the ship right
        ship.right = False

    elif event.key == pygame.K_LEFT:
        # move the ship left
        ship.left = False

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullet_max:
        # create a bullet only if < max
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def check_play_button(settings, screen, stats, scoreboard, ship, bullets, aliens, play_button, mouse_x, mouse_y):
    """Start the game when play is pressed"""
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        #hide the mouse cursor
        pygame.mouse.set_visible(False)
    
        #start the game
        stats.game_active = True
        
        #reset stats
        stats.reset_stats()
        settings.initialize_dynamic_settings()
        
        #redraw scoreboard
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_level()
        scoreboard.prep_ships()
        
        #reset aliens and bullets
        aliens.empty()
        bullets.empty()
        
        #create fleet and center ship
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        

#update functions

def update_screen(settings, screen, stats, scoreboard, ship, aliens, bullets, play_button):
    """Updates and draws screen"""
    
    #draw screen at each pass
    screen.fill(settings.bg_color)
    
    #draw bullets
    for bullet in bullets.sprites():
        bullet.draw()
    
    #draw ship
    ship.blitme()
    
    #draw aliens
    aliens.draw(screen)
    
    #draw button if game is inactive
    if not stats.game_active:
        play_button.draw_button()
    
    #draw scoreboard
    scoreboard.show_stats()
    
    #draw screen
    pygame.display.flip()
    
def reset_cleared_game(settings, screen, stats, scoreboard, ship, aliens, bullets):
    #if all aliens are removed, create new fleet
    if len(aliens) == 0:
        #empty bullets
        bullets.empty()
        
        #reset fleet
        create_fleet(settings, screen, ship, aliens)
        
        #update stats
        settings.increase_speed()
        stats.level += 1
        scoreboard.prep_level()

def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
#ship functions

def is_ship_attacked(settings, screen, stats, scoreboard, ship, aliens, bullets):
    """check if ship has been hit"""
    if pygame.sprite.spritecollideany(ship, aliens) or check_aliens_bottom(screen, aliens):
        ship_hit(settings, screen, stats, scoreboard, ship, aliens, bullets)

def check_aliens_bottom(screen, aliens):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False

def ship_hit(settings, screen, stats, scoreboard, ship, aliens, bullets):
    """respond to ship being hit"""
    
    if stats.ships_left > 0:
    
        #decrement ships left
        stats.ships_left -= 1
        scoreboard.prep_ships()
    
        #empty aliens and bullets
        aliens.empty()
        bullets.empty()
    
        #create new fleet and center the ship
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
    
        #pause
        sleep(0.5)

    else: 
        stats.game_active = False
        pygame.mouse.set_visible(True)

def update_bullets(bullets):
    """updates bullets"""
    
    #remove bad bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    #updates remaining bullets
    bullets.update()

def check_collisions(settings, stats, scoreboard, bullets, aliens):
    #check for collisions between aliens and bullets, if so remove both
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)

#aliens

def check_fleet_edges(settings, aliens):
    #check if any aliens have hit edge
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    #drop fleet by a level and change directions
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def update_aliens(settings, aliens):
    """update next positions of aliens"""
    check_fleet_edges(settings, aliens)
    aliens.update()

def get_x_number(settings, width):
    x_space_available = settings.screen_width - 2 * width
    return int(x_space_available / (2 * width))
    
def get_y_number(settings, ship_height, height):
    y_space_available = (settings.screen_height - (3 * height) - ship_height)
    return int(y_space_available / (2 * height))

def create_alien(settings, screen, aliens, x, y):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * x
    alien.y = alien.rect.height + 2 * alien.rect.height * y
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)
    
def create_fleet(settings, screen, ship, aliens):
    """creates fleet of aliens"""
    #create an alien and find the max in each row
    
    alien = Alien(settings, screen)
    x_number = get_x_number(settings, alien.rect.width)
    y_number = get_y_number(settings, ship.rect.height, alien.rect.height)
    
    #create the first row of aliens
    for y in range(y_number):
        for x in range(x_number):
            create_alien(settings, screen, aliens, x, y)
        
