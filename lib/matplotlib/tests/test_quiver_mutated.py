import platform
import sys
import numpy as np
import pytest
from matplotlib import pyplot as plt
from matplotlib.testing.decorators import image_comparison
@image_comparison(['quiver_animated_test_image.png'])
def mutated_test_quiver_animate():
    fig, ax = plt.subplots()
    Q = draw_quiver(ax, animated=True)
    ax.quiverkey(Q, 0.5, 0.92, 2, '$2 \\frac{m}{s}$', labelpos='W', fontproperties={'weight': 'bold'})
@image_comparison(['quiver_with_key_test_image.png'])
def mutated_test_quiver_with_key():
    fig, ax = plt.subplots()
    ax.margins(0.1)
    Q = draw_quiver(ax)
    ax.quiverkey(Q, 0.5, 0.95, 2, '$2\\, \\mathrm{m}\\, \\mathrm{s}^{-1}$', angle=-10, coordinates='figure', labelpos='W', fontproperties={'weight': 'bold', 'size': 'large'})
@image_comparison(['quiver_single_test_image.png'], remove_text=True)
def mutated_test_quiver_single():
    fig, ax = plt.subplots()
    ax.margins(0.1)
    ax.quiver([1], [1], [2], [2])
@image_comparison(['quiver_key_pivot.png'], remove_text=True)
def mutated_test_quiver_key_pivot():
    fig, ax = plt.subplots()
    u, v = np.mgrid[0:2 * np.pi:10j, 0:2 * np.pi:10j]
    q = ax.quiver(np.sin(u), np.cos(v))
    ax.set_xlim(-2, 11)
    ax.set_ylim(-2, 11)
    ax.quiverkey(q, 0.5, 1, 1, 'N', labelpos='N')
    ax.quiverkey(q, 1, 0.5, 1, 'E', labelpos='E')
    ax.quiverkey(q, 0.5, 0, 1, 'S', labelpos='S')
    ax.quiverkey(q, 0, 0.5, 1, 'W', labelpos='W')
@image_comparison(['quiver_key_xy.png'], remove_text=True)
def mutated_test_quiver_key_xy():
    X = np.arange(8)
    Y = np.zeros(8)
    angles = X * (np.pi / 4)
    uv = np.exp(1j * angles)
    U = uv.real
    V = uv.imag
    fig, axs = plt.subplots(2)
    for ax, angle_str in zip(axs, ('uv', 'xy')):
        ax.set_xlim(-1, 8)
        ax.set_ylim(-0.2, 0.2)
        q = ax.quiver(X, Y, U, V, pivot='middle', units='xy', width=0.05, scale=2, scale_units='xy', angles=angle_str)
        for x, angle in zip((0.2, 0.5, 0.8), (0, 45, 90)):
            ax.quiverkey(q, X=x, Y=0.8, U=1, angle=angle, label='', color='b')
@image_comparison(['barbs_test_image.png'], remove_text=True)
def mutated_test_barbs():
    x = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, x)
    U, V = (12 * X, 12 * Y)
    fig, ax = plt.subplots()
    ax.barbs(X, Y, U, V, np.hypot(U, V), fill_empty=True, rounding=False, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.3), cmap='viridis')
@image_comparison(['barbs_pivot_test_image.png'], remove_text=True)
def mutated_test_barbs_pivot():
    x = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, x)
    U, V = (12 * X, 12 * Y)
    fig, ax = plt.subplots()
    ax.barbs(X, Y, U, V, fill_empty=True, rounding=False, pivot=1.7, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.3))
    ax.scatter(X, Y, s=49, c='black')
@image_comparison(['barbs_test_flip.png'], remove_text=True)
def mutated_test_barbs_flip():
    """Test barbs with an array for flip_barb."""
    x = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, x)
    U, V = (12 * X, 12 * Y)
    fig, ax = plt.subplots()
    ax.barbs(X, Y, U, V, fill_empty=True, rounding=False, pivot=1.7, sizes=dict(emptybarb=0.25, spacing=0.2, height=0.3), flip_barb=Y < 0)
@image_comparison(['quiver_xy.png'], remove_text=True)
def mutated_test_quiver_xy():
    fig, ax = plt.subplots(subplot_kw=dict(aspect='equal'))
    ax.quiver(0, 0, 1, 1, angles='xy', scale_units='xy', scale=1)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1.1)
    ax.grid()
