import os
import subprocess

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

from colors import gruvbox_mat
from colors import gruvbox


@hook.subscribe.startup
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


@hook.subscribe.startup_once
def autostart_once():
    home = os.path.expanduser("~/.config/qtile/autostart_once.sh")
    subprocess.Popen([home])


mod = "mod1"
modalt = "mod4"
terminal = guess_terminal()

# Applicaton Variables
app_launcher = "rofi -show drun -disable-history -show-icons"
cmd_launcher = "rofi -show run -disable-history"
win_launcher = "rofi -show window -show-icons"

browser = "firefox"
file_manager = "pcmanfm"

screenshot = "flameshot full"
screenshot_gui = "flameshot gui"
lock = "betterlockscreen -l dimblur"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    # Window focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Rofi
    Key([mod], "space", lazy.spawn(app_launcher), desc="Application Launcher"),
    Key([mod], "w", lazy.spawn(win_launcher), desc="Application Launcher"),
    Key([mod], "c", lazy.spawn(cmd_launcher), desc="Application Launcher"),
    # Layout shifting
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Size shifting
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Volume
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume 0 +5%"),
        desc="Volume Up",
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume 0 -5%"),
        desc="volume down",
    ),
    Key(
        [], "XF86AudioMute", lazy.spawn("pulsemixer --toggle-mute"), desc="Volume Mute"
    ),
    # Media Control
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="playerctl"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="playerctl"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="playerctl"),
    # Brightness Control
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl s 10%+"),
        desc="brightness UP",
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl s 10%-"),
        desc="brightness Down",
    ),
    Key(
        [mod, "control"],
        "1",
        lazy.spawn("firefox"),
        desc="Run Firefox",
    ),
    Key(
        [mod, "control"],
        "2",
        lazy.spawn("alacritty -e ranger"),
        desc="Run Nautilus",
    ),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [
    Group("1", label="󰏃", matches=[Match(wm_class="firefox")]),
    Group("2", label="󰏃", matches=[Match(wm_class="chromium")]),
    Group("3", label="󰏃", matches=[Match(wm_class="Alacritty")]),
    Group("4", label="󰏃"),
    Group("5", label="󰏃"),
    Group("6", label="󰏃"),
    Group("7", label="󰏃"),
    Group("8", label="󰏃", matches=[Match(wm_class="Signal")]),
    Group("9", label="󰏃", matches=[Match(wm_class="Spotify")]),
]


for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4, margin=5),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()


def spacer(length):
    return widget.Spacer(length=length, background=gruvbox["dark-grey"])


def icon(name):
    pass


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    filename="~/.config/qtile/Assets/arch.png",
                    background=gruvbox["yellow"],
                    margin=3,
                ),
                spacer(12),
                widget.GroupBox(
                    fontsize=24,
                    borderwidth=3,
                    highlight_method="block",
                    active=gruvbox["cream-alt"],
                    block_highlight_text_color=gruvbox["yellow"],
                    highlight_color="#D0DAF0",
                    inactive=gruvbox["blue"],
                    foreground="#4B427E",
                    background=gruvbox["dark-grey"],
                    this_current_screen_border=gruvbox["dark-grey"],
                    this_screen_border=gruvbox["dark-grey"],
                    other_current_screen_border=gruvbox["dark-grey"],
                    other_screen_border=gruvbox["dark-grey"],
                    urgent_border=gruvbox["dark-grey"],
                    rounded=True,
                    disable_drag=True,
                ),
                spacer(10),
                widget.Image(
                    filename="~/.config/qtile/Assets/layout.png",
                    background=gruvbox["dark-grey"],
                ),
                widget.CurrentLayout(
                    background=gruvbox["dark-grey"],
                    foreground=gruvbox["cream"],
                    fmt="{}",
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/1.png",
                ),
                widget.WindowName(
                    background=gruvbox["dark-grey"],
                    format="{name}",
                    font="JetBrains Mono Bold",
                    fontsize=16,
                    foreground=gruvbox["yellow"],
                    empty_group_string="Desktop",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                spacer(10),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/ram.png",
                    background="#202222",
                ),
                widget.ThermalSensor(
                    background=gruvbox["dark-grey"],
                    foreground=gruvbox["cream-alt"],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    format="{temp: .0f}{unit}",
                    threshold=90.0,
                    update_interval=2,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                spacer(10),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/ram.png",
                    background="#202222",
                ),
                widget.CPU(
                    background="#202222",
                    foreground=gruvbox["cream-alt"],
                    format="{load_percent}%",
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=2,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/ram.png",
                    background="#202222",
                ),
                spacer(10),
                widget.Memory(
                    background="#202222",
                    format="{MemUsed: .0f} {mm}",
                    foreground=gruvbox["cream-alt"],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=2,
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                spacer(10),
                widget.Volume(
                    font="JetBrains Mono Bold",
                    fontsize=15,
                    theme_path="~/.config/qtile/Assets/Volume/",
                    emoji=True,
                    background="#202222",
                ),
                spacer(10),
                widget.Volume(
                    font="JetBrains Mono Bold",
                    fontsize=15,
                    background="#202222",
                    foreground=gruvbox["cream-alt"],
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/2.png",
                ),
                spacer(10),
                widget.Systray(
                    background=gruvbox["dark-grey"],
                    fontsize=2,
                ),
                spacer(10),
                widget.Image(
                    filename="~/.config/qtile/Assets/5.png",
                    background="#202222",
                ),
                widget.Image(
                    filename="~/.config/qtile/Assets/Misc/clock.png",
                    background="#0F1212",
                    margin_y=6,
                    margin_x=5,
                ),
                widget.Clock(
                    format="%I:%M %p",
                    background="#0F1212",
                    foreground=gruvbox["yellow-alt"],
                    font="JetBrains Mono Bold",
                    fontsize=15,
                ),
            ],
            40,
            border_color="#0F1212",
            border_width=[0, 0, 0, 0],
            margin=[10, 15, 6, 10],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
