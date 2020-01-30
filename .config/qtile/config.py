import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, hook, widget
from libqtile.widget import LaunchBar


from typing import List  # noqa: F401

mod = "mod4"
myTerm = "urxvt"


keys = [
    # Switch between windows in current stack pane
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),

    # Move windows up or down in current stack
    Key([mod, "control"], "h", lazy.layout.shuffle_left()),
    Key([mod, "control"], "j", lazy.layout.shuffle_down()),
    Key([mod, "control"], "k", lazy.layout.shuffle_up()),
    Key([mod, "control"], "l", lazy.layout.shuffle_right()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn(myTerm)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "q", lazy.window.kill()),

    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "d", lazy.spawn("rofi -modi drun -show drun")),
	Key([mod], "m", lazy.window.toggle_fullscreen()), # Toggle a window between minimum and maximum sizes
	Key([mod], "b", lazy.spawn("firefox")),  # Launch Firefox
	Key([mod], "p", lazy.spawn("bitwarden")), # Launch Bitwarden Password Manager
]

##### BAR COLORS #####
# Uses Tartan color scheme in xcolors.net from terminal.sexy
def init_colors():
    return [["#2e3436", "#2e3436"], # panel background
            ["#555753", "#555753"], # background for current screen tab
            ["#dedede", "#dedede"], # font color for group names
            ["#cc0000", "#cc0000"], # background color for layout widget
            ["#2b2b2b", "#2b2b2b"], # background for other screen tabs
            ["#8ae234", "#8ae234"], # dark green gradiant for other screen tabs
            ["#50fa7b", "#50fa7b"], # background color for network widget
            ["#4e9a06", "#4e9a06"], # background color for pacman widget
            ["#75507b", "#75507b"], # background color for cmus widget
            ["#3465a4", "#3465a4"], # background color for clock widget
            ["#06989a", "#06989a"]] # background color for systray widget


def init_group_names():
    return [("SYS", {'layout': 'monadtall'}),
	    ("MAIL", {'layout': 'monadtall'}),
	    ("AUD", {'layout': 'monadwide'}),
	    ("GAM", {'layout': 'floating'}),
	    ("WWW", {'layout': 'monadtall'}),
	    ("DOC", {'layout': 'monadtall'}),
	    ("CHAT", {'layout': 'monadtall'}),
	    ("MUS", {'layout': 'monadtall'})]


def init_groups():
    return [Group(name, **kwargs) for name, kwargs in group_names]

if __name__ in ["config", "__main__"]:
    group_names = init_group_names()
    groups = init_groups()

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))	# Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))  # Send current window to another group

##### LAYOUTS #####

def init_layout_theme():
    return {"border_width": 2,
            "margin": 4,
            "border_focus": "AD69AF",
            "border_normal": "1D2330"
           }

def init_layouts():
    return [layout.MonadTall(**layout_theme),
            layout.MonadWide(**layout_theme),
            layout.Bsp(**layout_theme),
            layout.Floating(border_focus="#3B4022")]

def init_widgets_defaults():
    return dict(font='sans',
                fontsize=10,
                padding=3,
                background = colors[2])

def init_widgets_list1():
    widgets_list1 = [
                widget.GroupBox(
                        visible_groups=['SYS', 'MAIL', 'AUD', 'GAM'],
                        active= colors[2],
                        inactive = colors[2],
                        highlight_method = "block",
                        foreground = colors[2],
                        background = colors[0]),
                widget.Prompt(),
                widget.WindowName(
                        foreground = colors[5],
                        background = colors[0],
                        padding = 5),
                widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[7],
                        padding =5),
                widget.TextBox(
                        text="🕪",
                        padding = 6,
                        foreground = colors[2],
                        background = colors[8]),
                widget.Volume(
                        foreground = colors[2],
                        background = colors[8],),
                widget.TextBox(
                        text="⟳",
                        foreground = colors[2],
                        background = colors[7]),
                widget.Pacman(
                        update_interval = 1800,
                        foreground = colors[2],
                        background = colors[7]),
                widget.Systray(
                        background=colors[10],
                        padding = 5),
                widget.Clock(
                        foreground = colors[2],
                        background = colors[9],
                        format="%A, %B %d - %H:%M"),
                widget.LaunchBar(progs=[
                        ('⏾', 'systemctl suspend', 'put computer to sleep')],
                        background = colors[0],
                        padding = 5, 
                        #default_icon='/usr/share/icons/Adwaita/24x24/status/night-light-symbolic.symbolic.png'
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 5,
                        background = colors[0],
                        ), 
                    ]
    return widgets_list1
    
def init_widgets_list2():
    widgets_list2 = [
                widget.GroupBox(
                        visible_groups=['WWW', 'DOC', 'CHAT', 'MUS'],
                        active= colors[2],
                        inactive = colors[2],
                        highlight_method = "block",
                        foreground = colors[2],
                        background = colors[0]),
                widget.WindowName(
                        foreground = colors[5],
                        background = colors[0],
                        padding = 5),
                widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[7],
                        padding =5),
                widget.TextBox(
                        text="🕪",
                        padding = 6,
                        foreground = colors[2],
                        background = colors[8]),
                widget.Volume(
                        foreground = colors[2],
                        background = colors[8],),
                widget.Clock(
                        foreground = colors[2],
                        background = colors[9],
                        format="%A, %B %d - %H:%M"),
                widget.LaunchBar(progs=[
                        ('⏾', 'systemctl suspend', 'put computer to sleep')],
                        background = colors[0],
                        padding = 5, 
                        #default_icon='/usr/share/icons/Adwaita/24x24/status/night-light-symbolic.symbolic.png'
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 5,
                        background = colors[0],
                        ), 
                    ]
    return widgets_list2 

##### SCREENS #####

def init_widgets_screen1():
	widgets_screen1 = init_widgets_list1()
	return widgets_screen1
	
def init_widgets_screen2():
	widgets_screen2 = init_widgets_list2()
	return widgets_screen2
	
def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.95, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.95, size=20))]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = False
focus_on_window_activation = "smart"

colors = init_colors()
screens = init_screens()
widget_defaults = init_widgets_defaults()
widgets_list1 = init_widgets_list1()
widgets_list2 = init_widgets_list2()
layout_theme = init_layout_theme()
layouts = init_layouts()
widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/bin/autostart.sh')
    subprocess.call(['sh', home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
