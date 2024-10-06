from PIL import Image


def towns_image_change_gif_to_png():
    path_to_files = '../towns_full_images_gif/'
    towns_name = ['Adventure_Map_Castle_citadel.gif',
                  'Adventure_Map_Castle_village.gif',
                  'Adventure_Map_Conflux_citadel.gif',
                  'Adventure_Map_Conflux_village.gif',
                  'Adventure_Map_Cove_citadel.gif',
                  'Adventure_Map_Cove_village.gif',
                  'Adventure_Map_Dungeon_citadel.gif',
                  'Adventure_Map_Dungeon_village.gif',
                  'Adventure_Map_Fortress_citadel.gif',
                  'Adventure_Map_Fortress_village.gif',
                  'Adventure_Map_Inferno_citadel.gif',
                  'Adventure_Map_Inferno_village.gif',
                  'Adventure_Map_Necropolis_citadel.gif',
                  'Adventure_Map_Necropolis_village.gif',
                  'Adventure_Map_Rampart_citadel.gif',
                  'Adventure_Map_Rampart_village.gif',
                  'Adventure_Map_Stronghold_citadel.gif',
                  'Adventure_Map_Stronghold_village.gif',
                  'Adventure_Map_Tower_citadel.gif',
                  'Adventure_Map_Tower_village.gif']

    for filename in towns_name:
        im = Image.open(path_to_files+filename)
        filename_without_git = filename.replace(".gif", "")
        im.save("towns_full_images_png/"+filename_without_git+".png", 'png', optimize=True, quality=70)


towns_image_change_gif_to_png()