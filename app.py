from stage_finder import find_reward_stage_from_start, play_stage
from stage_player import run_stage, return_to_home, check_completion, restart_stage
from time import sleep

if __name__ == "__main__":
  print("\033[2J")
  print("Initiating auto farm...")
  counter = 0
  while 1:
    map_name, pos = find_reward_stage_from_start()
    play_stage(pos)
    for i in range(4): # 4 tries per stage
      run_stage(map_name, verbosity=1)
      try:
        while not check_completion():
          sleep(4)
        break
      except Exception as e:
        print(e)
        restart_stage()
    else:
      print(f"Failed to complete stage {map_name}. Exiting...")
      exit(1)

    return_to_home()
    print("runs completed: ", counter := counter + 1)
