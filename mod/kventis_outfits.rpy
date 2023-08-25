
#
# █▄▀ █░█ ▀█▀		Originally made by ImKventis and maintained by Friends of Monika
# █░█ ▀▄▀ ░█░		https://github.com/ImKventis
#                    https://github.com/Friends-of-Monika
#


init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Outfit Selector",
        coauthors=["Friends of Monika", "MAS-Submod-MoyuTeam"],
        description="这个子模组可以让你保存一套装扮可以快速选择!",
        version="1.0.6"
    )

init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Outfit Selector",
            user_name="MAS-Submod-MoyuTeam",
            repository_name="MAS-Outfits"
        )

# Loading outfit jsons
# I'm not sure if 190 is the correct init level, but it works
init 190 python in kventis_outfit_submod:
    import os
    import json

    outfit_dir = os.path.join(renpy.config.basedir, "outfits")

    outfit_files = None

    try:
        outfit_files = os.listdir(outfit_dir)
    except:
        os.mkdir(outfit_dir)
        outfit_files = os.listdir(outfit_dir)



    outfits = {}

    outfit_menu_entries = []

    if len(outfit_files) != 0:
        for tf in outfit_files:
            # print tf
            if tf.endswith(".json") == False:
                continue
            try:
                f = open(os.path.join(outfit_dir, tf), "r")
                data = json.load(f)
                f.close()
                outfits[tf[:-5]] = data
                outfit_menu_entries.append((tf[:-5], tf[:-5], False, False))
                # print outfit_menu_entries[0][1]
            except Exception as e:
                # print e
                continue

# Should run once on install with high aff
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_installed_talk",
            prompt="你能跟我说说定制服装的事吗?",
            category=['衣服'],
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        markSeen=False
)

label monika_outfit_installed:
    m 1eua  "嘿, [player]."
    m 1wub "我发现你加了一些新东西! "
    extend 2dua "让我看看这里面有什么.{w=0.3}.{w=0.3}.{w=0.3}"
    m 3wua "噢!服装组合选择!"
    m 1eua "一定要替我感谢u/KventisAnM."
    m 3eua "还有,他让我给你捎口信. "
    extend 3sua "'如果你有任何关于此submod的意见或建议,你可以在reddit上给我留言.'"
    m 1gua "嗯,这不是很整洁嘛?诶嘿嘿~"
    m 1hua "谢谢你为我增加这些submod, [player]."
    m 1hubsb "我爱你!"
    return "love"

label monika_outfit_installed_talk:
    m 1eua "你想听听定制服装组合的事嘛?"
    m 1hua "好呀!"
    m 3eub "你可以随时跟我说,我会记住我现在穿的服装."
    m 3eub "这将会创建一个文件, {nw}"
    extend 1hub "这样我就可以读取出来穿给你看了!"
    m 1eua "如果你想让我穿一套你定制的衣服,就跟我说吧."
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_save",
            prompt="你可以保存一套服装嘛?",
            category=['外观', '衣服'],
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        markSeen=False
    )

label monika_outfit_save:
    $ import json
    $ import os

    m 1hua "好啊!"

    label ostart:
        pass

    # Get nae for file
    $ done = False
    while not done:
        python:
            out_name = ""
            out_name = mas_input(
                    "为这套衣服输入名字:",
                    #allow="abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                    )

        #Check if we should return
        if out_name == "cancel_input":
            m 1euc "喔,好的."
            return "prompt"
        elif out_name == "":
            m 2lusdla "..."
            m 1eka "我很抱歉,我记不住一套没有名字的衣服,[player]."
        else:
            $ done = True

    python:
        outfit_file = os.path.join(kventis_outfit_submod.outfit_dir, out_name + ".json")

        file_exists = os.access(
                os.path.normcase(outfit_file),
                os.F_OK
            )

    $ overwrite = False

    if file_exists:
        m 1eka "我已经有一套叫做'[out_name]'的服装组合了"
        m "我要覆盖它嘛?{nw}"
        $ _history_list.pop()
        menu:
            m "我要覆盖它嘛?{fast}"

            "是的.":
                $ overwrite = True

            "不要哦.":
                # Jump to beginning
                jump ostart

    m 2dua "等我一下.{w=0.3}.{w=0.3}."
    python:
        out_data = {
            "hair": monika_chr.hair.name,
            "clothes": monika_chr.clothes.name,
        }

        # Much cleaner
        acs = monika_chr.acs[0] + monika_chr.acs[1] + monika_chr.acs[3] + monika_chr.acs[4] + monika_chr.acs[5] + monika_chr.acs[6] + monika_chr.acs[7] + monika_chr.acs[8] + monika_chr.acs[9] + monika_chr.acs[10] + monika_chr.acs[11] + monika_chr.acs[12] + monika_chr.acs[13]
        # Needs names not classes
        acs = map(lambda arg: arg.name, acs)
        out_data["acs"] = acs

        saved = False
        try:
            with open(outfit_file, "w+") as out_file:
                json.dump(out_data, out_file)
                out_file.close()

            kventis_outfit_submod.outfits[out_name] = out_data
            if overwrite == False:
                kventis_outfit_submod.outfit_menu_entries.append((out_name, out_name, False, False))
                saved = True
            saved = True
        except Exception as e:
            saved = False

    if saved:
        m 3eub "我记住了!"
        return
    else:
        m 2eksdlc "我很抱歉[player],可能是因为sub格式的要求,我记不住这一套服装."
        m 1eksdlc "也许你可以试试用其他的名字?"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_load",
            prompt="你可以穿一套衣服吗?",
            category=['外观', '衣服'],
            pool=True,
            aff_range=(mas_aff.NORMAL, None),
            unlocked=True
        ),
        markSeen=False
    )

# Needs testing
label monika_outfit_missing:
    m "[player]..."
    m "我找不到这套衣服之中的一部分了!"
    m "是你把它们删掉了吗?"
    call mas_transition_from_emptydesk
    pause 1
    m 2dkd "我真的很喜欢那一套衣服..."
    m 2ekd "请再把它装回来!"
    return

# Needs testing
label monika_outfit_done_no_acs:

    $ import random

    pause 2

    m "好的."

    call mas_transition_from_emptydesk

    pause 0.5

    m 4eublb "Ta-da!~"

    m 1euc "我找不到其中的配饰!"

    m 1ekc "请务必再加一次."
    return


label monika_outfit_done:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 1

    m 4eublb "Ta-da!~"

    # Cba to write quips tbh
    # $ quip = random.choice(kventis_outfit_submod.outfit_quips)

    # # Nomrmal "M "Dialoug"" wouldnt format quips for some reason
    # $ renpy.say(m, quip)
    return

label monika_outfit_load:

    m 1hua "当然啦!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m 1eub "你要我穿哪件衣服?" nointeract

        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("算了", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m 1euc "喔...好吧."
            return "prompt"

        m 2dua "稍微等我一下..."

        call mas_transition_to_emptydesk

        pause 2

        python:
            # Get all atrributes of outfit fills with None if missing
            # Dont have to check if new_clothes and new_hair in json dict as they always are.
            sel_outfit = kventis_outfit_submod.outfits[sel_outfit_name]
            new_clothes = mas_sprites.CLOTH_MAP.get(sel_outfit.get("clothes"), None)
            new_hair = mas_sprites.HAIR_MAP.get(sel_outfit.get("hair"), None)
            new_acs = monika_chr.acs[2]
            missing_acs = False

            for item in sel_outfit.get("acs", []):
                new_item = mas_sprites.ACS_MAP.get(item, None)
                if new_item != None:
                    new_acs.append(new_item)
                else:
                    missing_acs = True

        # Game assessts r missing
        if new_clothes == None or new_hair == None:
            call monika_outfit_missing
            return

        python:
            monika_chr.remove_all_acs()
            monika_chr.change_clothes(new_clothes, True)
            monika_chr.change_hair(new_hair, True)
            # Applies all acs including the acs that were already on the table
            for ac in new_acs:
                monika_chr.wear_acs(ac)

        if missing_acs:
            call monika_outfit_done_no_acs
            return
        else:
            call monika_outfit_done
        return
    else:
        m 1euc "哦等等."
        m 3lksdlb "啊哈!我还没穿好衣服呢."
        m 1eub "如果你想保存一套衣服，请告诉我!"
        return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_delete",
            prompt="你可以删除一套衣服吗?",
            category=['外观', '衣服'],
            pool=True,
            aff_range=(mas_aff.NORMAL, None),
            unlocked=True
        ),
        markSeen=False
    )

label monika_outfit_delete:
    $ import os
    m 1hua "好啊!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m 1eub "你想让我删除哪一套衣服?" nointeract

        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("算了", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m 1etc "好吧,{w=0.4} {nw}"
            extend 1hua "那我就不删啦!"
            return "prompt"

        m 1eksdlc "你确定你想删除[sel_outfit_name], [player]? "
        extend "这可撤销不了哦!{nw}"
        $ _history_list.pop()
        menu:
            m "你确定你想删除[sel_outfit_name], [player]?这可撤销不了哦!{fast}"
            "当然":
                m "Okie-doki."
                python:
                    removed = False
                    try:
                        os.remove(os.path.join(kventis_outfit_submod.outfit_dir, sel_outfit_name + ".json"))
                        kventis_outfit_submod.outfit_menu_entries.remove((sel_outfit_name, sel_outfit_name, False, False))
                        kventis_outfit_submod.outfits.pop(sel_outfit_name)
                        removed = True
                    except:
                        removed = False
                m 2dua "稍等.{w=0.3}.{w=0.3}."
                if removed:
                    m 3eub "[sel_outfit_name]已经被删掉了哦!"
                else:
                    m 1euc "我找不到[sel_outfit_name]的文件!"
                    m 3lksdlb "你可以自己粗暴地从文件夹中删除它. "
                    m extend "它在outfits文件夹里叫'[sel_outfit_name].json'!"
                return

            "等一下,我得想想.":
                m 1eusdlb "哦, okay."
                return
    else:
        m 1euc "哦等一下."
        m 3lksdlb "啊-哈...!我还没有保存任何服装."
        m 1eub "如果你想保存一套衣服，请告诉我."
        return

# G'day
# - British man
