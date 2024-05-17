from utils import Image, resize_img, g_w

map_box = Image.open('asset/map_box.png')
reward_icon = Image.open('asset/bonus_reward.png')
toggle_map_icon = Image.open('asset/expert.png')
enter_level_select_icon = Image.open('asset/enter_level_select.png')
expert_page_1_icon = Image.open('asset/expert_page_1.png')
easy_icon = Image.open('asset/difficulty_easy.png')
start_stage_icon = Image.open('asset/start_stage.png')
stage_loaded_check_icon = Image.open('asset/stage_loaded.png')
success_next_icon = Image.open('asset/success_next.png')
success_home_icon = Image.open('asset/success_home.png')
collect_icon = Image.open('asset/collect.png')
insta_icon = Image.open('asset/insta_common.png')
reward_continue_icon = Image.open('asset/reward_continue.png')
back_icon = Image.open('asset/back.png')
overwrite_ok_icon = Image.open('asset/overwrite_ok.png')
level_up_icon = Image.open('asset/level_up.png')
defeat_icon = Image.open('asset/defeat.png')
restart_icon = Image.open('asset/restart_confirm.png')
restart_btn_icon = Image.open('asset/restart_btn.png')
# assets r in window size of 1280x720
scale = g_w / 1280

# stage_finder assets
reward_icon = resize_img(reward_icon, scale)
toggle_map_icon = resize_img(toggle_map_icon, scale)
map_box = resize_img(map_box, scale)
enter_level_select_icon = resize_img(enter_level_select_icon, scale)
expert_page_1_icon = resize_img(expert_page_1_icon, scale)
easy_icon = resize_img(easy_icon, scale)
start_stage_icon = resize_img(start_stage_icon, scale)
stage_loaded_check_icon = resize_img(stage_loaded_check_icon, scale)
overwrite_ok_icon = resize_img(overwrite_ok_icon, scale)

# stage_player assets
success_next_icon = resize_img(success_next_icon, scale)
success_home_icon = resize_img(success_home_icon, scale)
collect_icon = resize_img(collect_icon, scale)
insta_icon = resize_img(insta_icon, scale)
reward_continue_icon = resize_img(reward_continue_icon, scale)
back_icon = resize_img(back_icon, scale)
level_up_icon = resize_img(level_up_icon, scale)
defeat_icon = resize_img(defeat_icon, scale)
restart_icon = resize_img(restart_icon, scale)
restart_btn_icon = resize_img(restart_btn_icon, scale)

# instamonkey coordinates recorded in 1280x720 window size
insta_xy = [
  [scale * 958, 275 * scale],
  [scale * 1040, 275 * scale],
  [scale * 1040, 351 * scale],
  [scale * 958, 351 * scale],
]

