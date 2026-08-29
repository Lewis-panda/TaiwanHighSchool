# -*- coding: utf-8 -*-
"""重生「數B4-1 空間概念與圓錐曲線」學生講義的章內 SVG。"""

if __name__ == "__main__" and __import__("sys").argv[1:]:
    raise SystemExit("本腳本不接受參數；直接執行即可重生數B4-1 章內 SVG。")

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, Ellipse, Polygon, Rectangle, Wedge
import numpy as np

import figlib as F


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAPTER = os.path.join(ROOT, "content", "數學B", "數B4-1")

FIGURE_OUTPUTS = (
    ("fig_line_relations", "數B4-1-空間兩直線關係.svg"),
    ("fig_line_plane", "數B4-1-直線與平面垂直.svg"),
    ("fig_dihedral", "數B4-1-兩面角量測.svg"),
    ("fig_box_paths", "數B4-1-長方體表面路徑.svg"),
    ("fig_solid_nets", "數B4-1-圓錐與圓錐臺展開.svg"),
    ("fig_cube_sections", "數B4-1-正立方體截面.svg"),
    ("fig_space_coordinates", "數B4-1-空間坐標與投影.svg"),
    ("fig_distance_decomposition", "數B4-1-空間距離分解.svg"),
    ("fig_sphere_plane", "數B4-1-球面與平面截痕.svg"),
    ("fig_globe_coordinates", "數B4-1-經緯度與空間坐標.svg"),
    ("fig_great_circle", "數B4-1-弦長與大圓弧長.svg"),
    ("fig_conic_gallery", "數B4-1-圓錐曲線方程圖.svg"),
    ("fig_cone_cuts", "數B4-1-圓錐截痕分類.svg"),
    ("fig_degenerate_cuts", "數B4-1-退化圓錐截痕.svg"),
    ("fig_parabola_focus", "數B4-1-拋物線反射.svg"),
    ("fig_ellipse_reflection", "數B4-1-橢圓焦點反射.svg"),
)


def _save(fig, filename):
    stem, extension = os.path.splitext(filename)
    if extension != ".svg" or not stem.startswith("數B4-1-"):
        raise AssertionError("輸出檔名必須是數B4-1 章內 SVG")
    return F.save_to(fig, CHAPTER, stem, output_subdir="assets", write_pdf=False)


def _point(ax, p, label, *, color=F.INK, dx=.08, dy=.10, size=32):
    ax.scatter([p[0]], [p[1]], color=color, s=size, zorder=8)
    ax.text(p[0] + dx, p[1] + dy, label, color=color, fontsize=10.5, zorder=9)


def _proj3(points):
    """固定斜投影，保留各圖相同的坐標方向。"""
    p = np.asarray(points, dtype=float)
    x = p[..., 0] - .64 * p[..., 1]
    y = p[..., 2] + .38 * p[..., 1]
    return np.stack([x, y], axis=-1)


def _draw_box(ax, lengths=(4., 3., 2.5), *, labels=True, color=F.INK):
    a, b, c = lengths
    vertices = np.array([[0,0,0],[a,0,0],[a,b,0],[0,b,0],
                         [0,0,c],[a,0,c],[a,b,c],[0,b,c]], dtype=float)
    q = _proj3(vertices)
    edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
             (0,4),(1,5),(2,6),(3,7)]
    for i, j in edges:
        ax.plot(q[[i,j],0], q[[i,j],1], color=color, lw=1.5,
                ls="--" if (i,j) in ((2,3),(3,0),(3,7)) else "-")
    if labels:
        names = "ABCDEFGH"
        for p, name in zip(q, names):
            _point(ax, p, f"${name}$", dx=.06, dy=.08, size=24)
    return vertices, q


def fig_line_relations():
    vertices = np.array([[0,0,0],[4,0,0],[4,3,0],[0,3,0],
                         [0,0,2.5],[4,0,2.5],[4,3,2.5],[0,3,2.5]], dtype=float)
    ab = vertices[1]-vertices[0]
    ef = vertices[5]-vertices[4]
    bc = vertices[2]-vertices[1]
    cg = vertices[6]-vertices[2]
    assert np.allclose(np.cross(ab, ef), 0)
    assert math.isclose(np.dot(ab, bc), 0)
    assert not np.allclose(np.cross(ab, cg), 0)

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    titles = ["平行：$AB\\parallel EF$", "相交且垂直：$AB\\perp BC$", "歪斜：$AB$ 與 $CG$"]
    pairs = [((0,1),(4,5),F.BLUE), ((0,1),(1,2),F.GREEN), ((0,1),(2,6),F.RED)]
    for ax, title, (e1,e2,color) in zip(axes, titles, pairs):
        _, q = _draw_box(ax)
        for i,j in (e1,e2):
            ax.plot(q[[i,j],0], q[[i,j],1], color=color, lw=4, solid_capstyle="round")
        ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=12)
    fig.suptitle("先檢查是否共平面，再判斷相交、平行或歪斜", fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-空間兩直線關係.svg")


def fig_line_plane():
    foot = np.array([0., 0.]); a = np.array([2.4, .7]); b = np.array([-.8, 1.8])
    assert abs(np.linalg.det(np.column_stack([a,b]))) > 1
    vertical = np.array([0., 3.2])
    fig, ax = F.canvas(9.2, 5.2, equal=True)
    plane = np.array([[-3,-1.25],[3,-1.25],[4,1.15],[-2,1.15]])
    ax.add_patch(Polygon(plane, closed=True, facecolor=F.FILL, edgecolor=F.GRID, alpha=.25))
    ax.plot([-2.4,2.8],[-.75,.75], color=F.BLUE, lw=2.2, label="$m$")
    ax.plot([-1.3,1.6],[.9,-1.0], color=F.GREEN, lw=2.2, label="$n$")
    ax.plot([0,0],[0,3.2], color=F.RED, lw=3)
    _point(ax, foot, "$P$", dx=.12, dy=-.42)
    ax.text(.18, 2.35, "$L$", color=F.RED, fontsize=13)
    ax.text(-3.2,-1.55,"平面 $E$", color=F.INK, fontsize=12)
    ax.add_patch(Rectangle((0,-.02), .34, .34, angle=16, fill=False, edgecolor=F.RED, lw=1.4))
    ax.add_patch(Rectangle((-.02,-.02), .30, .30, angle=-33, fill=False, edgecolor=F.RED, lw=1.4))
    ax.text(-3.1,2.65,"$m,n$ 在 $E$ 上相交於 $P$\n$L\\perp m$ 且 $L\\perp n$\n$\\Longrightarrow L\\perp E$", fontsize=12)
    ax.set_xlim(-4.1,4.2); ax.set_ylim(-1.9,3.8); ax.axis("off")
    ax.set_title("兩條相交方向鎖定整個平面")
    fig.tight_layout()
    return _save(fig, "數B4-1-直線與平面垂直.svg")


def fig_dihedral():
    theta = math.radians(120)
    ray_a = 1.8*np.array([math.cos(math.radians(-60)), math.sin(math.radians(-60))])
    ray_b = 1.8*np.array([math.cos(math.radians(60)), math.sin(math.radians(60))])
    assert math.isclose(np.dot(ray_a,ray_b)/(np.linalg.norm(ray_a)*np.linalg.norm(ray_b)), math.cos(theta))
    fig, ax = F.canvas(9.2, 5.4, equal=True)
    hinge = np.array([[-3.2,0],[3.2,0]])
    p1 = np.array([[-3.2,0],[3.2,0],[2.2,-1.65],[-2.2,-1.65]])
    p2 = np.array([[-3.2,0],[3.2,0],[2.35,1.8],[-2.35,1.8]])
    ax.add_patch(Polygon(p1, facecolor=F.BLUE, alpha=.10, edgecolor=F.BLUE))
    ax.add_patch(Polygon(p2, facecolor=F.GREEN, alpha=.11, edgecolor=F.GREEN))
    ax.plot(hinge[:,0], hinge[:,1], color=F.INK, lw=3)
    ax.text(2.9,.14,"交線 $L$", fontsize=11)
    F.arrow(ax, (0,0), ray_a, color=F.BLUE)
    F.arrow(ax, (0,0), ray_b, color=F.GREEN)
    ax.add_patch(Arc((0,0), 1.35, 1.35, theta1=-60, theta2=60, color=F.RED, lw=2))
    ax.text(.72,-.02,"$\\theta$", color=F.RED, fontsize=13)
    ax.text(-3.0,-1.28,"$E_1$ 內射線 $PA\\perp L$", color=F.BLUE)
    ax.text(-2.8,1.28,"$E_2$ 內射線 $PB\\perp L$", color=F.GREEN)
    _point(ax, (0,0), "$P$", dx=.12, dy=.12)
    ax.set_xlim(-3.7,3.8); ax.set_ylim(-2.1,2.25); ax.axis("off")
    ax.set_title("兩面角量在垂直交線的共同截面上")
    fig.tight_layout()
    return _save(fig, "數B4-1-兩面角量測.svg")


def fig_box_paths():
    a,b,c = 6.,4.,3.
    candidates = [math.hypot(a+b,c), math.hypot(a+c,b), math.hypot(b+c,a)]
    assert np.allclose(candidates, [math.sqrt(109), math.sqrt(97), math.sqrt(85)])
    assert min(candidates) == candidates[2]
    fig, axes = plt.subplots(1,3,figsize=(12,4.2))
    dims = [((a+b,c),"$\\sqrt{(6+4)^2+3^2}=\\sqrt{109}$"),
            ((a+c,b),"$\\sqrt{(6+3)^2+4^2}=\\sqrt{97}$"),
            ((b+c,a),"$\\sqrt{(4+3)^2+6^2}=\\sqrt{85}$")]
    for ax, ((w,h), label) in zip(axes,dims):
        ax.add_patch(Rectangle((0,0),w,h,facecolor=F.FILL,alpha=.15,edgecolor=F.INK))
        ax.plot([0,w],[0,h],color=F.RED,lw=2.8)
        _point(ax,(0,0),"$A$",dx=.1,dy=.12); _point(ax,(w,h),"$G$",dx=-.35,dy=-.45)
        ax.text(w/2,-.7,label,ha="center",fontsize=11)
        ax.set_xlim(-.5,w+.5); ax.set_ylim(-1.0,h+.6); ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle("相對頂點有三類展開；比較三條平面對角線",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-長方體表面路徑.svg")


def fig_solid_nets():
    r, slant = 2., 5.
    theta = 2*math.pi*r/slant
    assert math.isclose(slant*theta,2*math.pi*r)
    assert math.isclose(.5*slant*slant*theta,math.pi*r*slant)
    r1,r2,s = 1.5,3.0,4.0
    inner,outer = 4.0,8.0
    frustum_theta = 3*math.pi/4
    assert math.isclose(outer-inner,s)
    assert math.isclose(outer/inner,r2/r1)
    assert math.isclose(outer*frustum_theta,2*math.pi*r2)
    assert math.isclose(inner*frustum_theta,2*math.pi*r1)
    assert math.isclose(.5*frustum_theta*(outer**2-inner**2),math.pi*(r1+r2)*s)
    fig, axes = plt.subplots(1,2,figsize=(11.5,5.0))
    ax=axes[0]; ax.set_aspect("equal"); ax.axis("off")
    deg=math.degrees(theta)
    ax.add_patch(Wedge((0,0),slant,0,deg,facecolor=F.BLUE,alpha=.14,edgecolor=F.BLUE,lw=2))
    ax.add_patch(Circle((8.0,1.8),r,facecolor=F.GREEN,alpha=.14,edgecolor=F.GREEN,lw=2))
    ax.text(1.7,2.0,"側面扇形",color=F.BLUE); ax.text(8.0,1.75,"底面",ha="center",color=F.GREEN)
    ax.text(2.0,-.55,"弧長 $R\\theta=2\\pi r$\n側面積 $\\pi Rr$",ha="center")
    ax.set_xlim(-.7,10.4); ax.set_ylim(-1.2,5.6); ax.set_title("直圓錐")
    ax=axes[1]; ax.set_aspect("equal"); ax.axis("off")
    angle=math.degrees(frustum_theta)
    ax.add_patch(Wedge((0,0),outer,0,angle,width=outer-inner,facecolor=F.AMBER,alpha=.18,edgecolor=F.AMBER,lw=2))
    ax.text(1.1,3.6,"大扇形減小扇形",color=F.AMBER)
    ax.text(1.8,-.55,"側面積 $\\pi(r_1+r_2)s$\n$=18\\pi$",ha="center")
    ax.set_xlim(-1,8.6); ax.set_ylim(-1.2,8.7); ax.set_title("直圓錐臺")
    fig.suptitle("展開後的弧長必須接回底面圓周",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-圓錐與圓錐臺展開.svg")


def _cube_plane_intersections(normal, d):
    vertices=np.array([[x,y,z] for x in (0.,1.) for y in (0.,1.) for z in (0.,1.)])
    edges=[]
    for i,a in enumerate(vertices):
        for j,b in enumerate(vertices):
            if j>i and np.count_nonzero(np.abs(a-b)>.5)==1:
                edges.append((a,b))
    pts=[]
    for a,b in edges:
        va=np.dot(normal,a)-d; vb=np.dot(normal,b)-d
        if abs(va)<1e-9: pts.append(a)
        if va*vb<0:
            t=va/(va-vb); pts.append(a+t*(b-a))
    unique=[]
    for p in pts:
        if not any(np.linalg.norm(p-q)<1e-7 for q in unique): unique.append(p)
    return np.array(unique)


def fig_cube_sections():
    tri=_cube_plane_intersections(np.array([1.,1.,1.]),.72)
    hexagon=_cube_plane_intersections(np.array([1.,1.,1.]),1.5)
    assert len(tri)==3 and len(hexagon)==6
    fig,axes=plt.subplots(1,2,figsize=(10.5,4.8))
    for ax,pts,title,color in ((axes[0],tri,"靠近頂點：三角形",F.BLUE),(axes[1],hexagon,"通過六條稜：六邊形",F.RED)):
        _,q=_draw_box(ax,lengths=(1,1,1),labels=False,color=F.GRID)
        qp=_proj3(pts)
        center=qp.mean(axis=0); angles=np.arctan2(qp[:,1]-center[1],qp[:,0]-center[0]); qp=qp[np.argsort(angles)]
        ax.add_patch(Polygon(qp,closed=True,facecolor=color,alpha=.25,edgecolor=color,lw=2.5))
        ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title)
        ax.set_xlim(-.9,1.2); ax.set_ylim(-.15,1.55)
    fig.suptitle("截面頂點落在立體的稜上；同一面內依序連線",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-正立方體截面.svg")


def fig_space_coordinates():
    p=np.array([3.,2.,4.])
    projections={"$xy$":np.array([3.,2.,0.]),"$yz$":np.array([0.,2.,4.]),"$xz$":np.array([3.,0.,4.])}
    assert np.allclose(projections["$xy$"],[p[0],p[1],0])
    fig,ax=F.canvas(9.4,6.0,equal=True)
    o=_proj3([[0,0,0]])[0]; x=_proj3([[4.4,0,0]])[0]; y=_proj3([[0,3.5,0]])[0]; z=_proj3([[0,0,5]])[0]
    F.arrow(ax,o,x,color=F.BLUE); F.arrow(ax,o,y,color=F.GREEN); F.arrow(ax,o,z,color=F.RED)
    ax.text(x[0]+.1,x[1],"$x$"); ax.text(y[0]-.25,y[1]+.1,"$y$"); ax.text(z[0]+.1,z[1],"$z$")
    qp=_proj3([p])[0]; _point(ax,qp,"$P(3,2,4)$",color=F.PURPLE,dx=.15,dy=.15,size=45)
    colors=[F.BLUE,F.GREEN,F.AMBER]
    for (name,q3),color in zip(projections.items(),colors):
        q=_proj3([q3])[0]; ax.plot([qp[0],q[0]],[qp[1],q[1]],color=color,ls="--",lw=1.8)
        _point(ax,q,name,color=color,dx=.07,dy=.08)
    ax.text(-.35,3.15,"投到坐標平面：\n垂直方向的坐標改成 0",fontsize=11.5,ha="right")
    ax.set_xlim(-3.2,4.8); ax.set_ylim(-.7,5.2); ax.axis("off")
    ax.set_title("右手坐標系與三個正射影")
    fig.tight_layout()
    return _save(fig, "數B4-1-空間坐標與投影.svg")


def fig_distance_decomposition():
    p=np.array([1.,2.,4.]); q=np.array([5.,5.,1.]); delta=q-p
    assert np.allclose(delta,[4,3,-3])
    assert math.isclose(np.linalg.norm(delta),math.sqrt(34))
    pts=np.array([p,[q[0],p[1],p[2]],[q[0],q[1],p[2]],q])
    r=_proj3(pts)
    fig,ax=F.canvas(9.5,5.5,equal=True)
    cols=[F.BLUE,F.GREEN,F.AMBER]
    labels=["$\\Delta x=4$","$\\Delta y=3$","$\\Delta z=-3$"]
    for i in range(3):
        F.arrow(ax,r[i],r[i+1],color=cols[i]); ax.text(*(r[i]+r[i+1])/2,labels[i],color=cols[i],fontsize=11)
    ax.plot([r[0,0],r[-1,0]],[r[0,1],r[-1,1]],color=F.RED,lw=2.8)
    _point(ax,r[0],"$P(1,2,4)$",dx=-.9,dy=.2); _point(ax,r[-1],"$Q(5,5,1)$",dx=.12,dy=.1)
    ax.text(.7,-.35,"$PQ=\\sqrt{4^2+3^2+(-3)^2}=\\sqrt{34}$",color=F.RED,fontsize=13)
    # The projected y-component reaches 5.9; keep the whole green segment and
    # its label inside the axes so the three-component decomposition is visible.
    ax.set_xlim(-2.2,5.6); ax.set_ylim(-.8,6.4); ax.axis("off")
    ax.set_title("三個互相垂直的坐標差形成空間畢氏定理")
    fig.tight_layout()
    return _save(fig, "數B4-1-空間距離分解.svg")


def fig_sphere_plane():
    R,d=5.,3.; r=math.sqrt(R*R-d*d)
    assert math.isclose(r,4.)
    fig,axes=plt.subplots(1,3,figsize=(12,4.3))
    cases=[(6.,"$d>R$：沒有交點",F.GRID),(5.,"$d=R$：相切一點",F.AMBER),(3.,"$d<R$：截圓半徑 4",F.BLUE)]
    for ax,(dist,title,color) in zip(axes,cases):
        ax.add_patch(Circle((0,0),R,fill=False,edgecolor=F.INK,lw=1.8))
        ax.plot([-5.8,5.8],[dist,dist],color=color,lw=2.2)
        if dist<R:
            rr=math.sqrt(R*R-dist*dist); ax.plot([-rr,rr],[dist,dist],color=F.RED,lw=4)
            ax.plot([0,0],[0,dist],color=F.GREEN,ls="--")
            ax.plot([0,rr],[0,dist],color=F.PURPLE,ls="--")
            ax.text(.25,1.3,"$d=3$"); ax.text(1.8,1.1,"$R=5$"); ax.text(1.4,3.25,"$r=4$",color=F.RED)
        ax.set_xlim(-6,6); ax.set_ylim(-5.8,7); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title,fontsize=11)
    fig.suptitle("球心到平面的距離決定交集；$r=\\sqrt{R^2-d^2}$",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-球面與平面截痕.svg")


def fig_globe_coordinates():
    R=4.; lon=math.radians(120); lat=math.radians(30)
    p=np.array([R*math.cos(lat)*math.cos(lon),R*math.cos(lat)*math.sin(lon),R*math.sin(lat)])
    expected=np.array([-math.sqrt(3),3.,2.])
    assert np.allclose(p,expected)
    q=np.array([p[0],p[1],0.])
    assert np.allclose(q,[-math.sqrt(3),3,0])
    fig,ax=F.canvas(9.5,6.1,equal=True)
    t=np.linspace(0,2*math.pi,500)
    equator=np.column_stack([R*np.cos(t),R*np.sin(t),np.zeros_like(t)])
    meridian=np.column_stack([R*np.cos(t),np.zeros_like(t),R*np.sin(t)])
    lat_circle=np.column_stack([R*math.cos(lat)*np.cos(t),R*math.cos(lat)*np.sin(t),np.full_like(t,R*math.sin(lat))])
    for curve,color,style,width in ((equator,F.GRID,"--",1.4),(meridian,F.GRID,"--",1.2),(lat_circle,F.BLUE,"-",1.8)):
        qq=_proj3(curve); ax.plot(qq[:,0],qq[:,1],color=color,ls=style,lw=width)
    o=_proj3([[0,0,0]])[0]
    for endpoint,label,color in (([5,0,0],"$x$",F.BLUE),([0,5,0],"$y$",F.GREEN),([0,0,5],"$z$",F.RED)):
        end=_proj3([endpoint])[0]; F.arrow(ax,o,end,color=color); ax.text(end[0]+.08,end[1]+.08,label,color=color)
    pp=_proj3([p])[0]; qq=_proj3([q])[0]
    _point(ax,pp,r"$P(-\sqrt{3},3,2)$",color=F.RED,dx=.15,dy=.15,size=42)
    _point(ax,qq,"$Q$",color=F.GREEN,dx=.12,dy=-.35)
    ax.plot([o[0],qq[0]],[o[1],qq[1]],color=F.GREEN,lw=2)
    ax.plot([qq[0],pp[0]],[qq[1],pp[1]],color=F.RED,ls="--",lw=2)
    lon_t=np.linspace(0,lon,100)
    lon_arc=np.column_stack([1.1*np.cos(lon_t),1.1*np.sin(lon_t),np.zeros_like(lon_t)])
    la=_proj3(lon_arc); ax.plot(la[:,0],la[:,1],color=F.GREEN,lw=2)
    q_unit=q[:2]/np.linalg.norm(q[:2]); lat_t=np.linspace(0,lat,80)
    lat_arc=np.column_stack([1.45*np.cos(lat_t)*q_unit[0],1.45*np.cos(lat_t)*q_unit[1],1.45*np.sin(lat_t)])
    lq=_proj3(lat_arc); ax.plot(lq[:,0],lq[:,1],color=F.RED,lw=2)
    ax.text(-.25,.55,"$120^\\circ$",color=F.GREEN); ax.text(-1.35,1.35,"$30^\\circ$",color=F.RED)
    ax.text(-3.8,-1.25,r"$P=(R\cos\varphi\cos\theta,\ R\cos\varphi\sin\theta,\ R\sin\varphi)$",fontsize=12)
    ax.set_xlim(-4.4,5.2); ax.set_ylim(-1.55,6.0); ax.axis("off")
    ax.set_title("經度決定赤道面方向；緯度決定高度")
    fig.tight_layout()
    return _save(fig, "數B4-1-經緯度與空間坐標.svg")


def fig_great_circle():
    R=4.; theta=math.radians(120)
    chord=2*R*math.sin(theta/2); arc=R*theta
    assert math.isclose(chord,4*math.sqrt(3)); assert math.isclose(arc,8*math.pi/3); assert arc>chord
    a=np.array([R,0.]); b=R*np.array([math.cos(theta),math.sin(theta)])
    fig,ax=F.canvas(8.7,5.5,equal=True)
    ax.add_patch(Circle((0,0),R,fill=False,edgecolor=F.INK,lw=1.8))
    ax.plot([a[0],b[0]],[a[1],b[1]],color=F.BLUE,lw=2.6)
    ang=np.linspace(0,theta,120); ax.plot(R*np.cos(ang),R*np.sin(ang),color=F.RED,lw=3.0)
    F.arrow(ax,(0,0),a,color=F.GRID); F.arrow(ax,(0,0),b,color=F.GRID)
    F.angle_arc(ax,(0,0),1.1,0,120,color=F.GREEN,text="$120^\\circ$")
    _point(ax,a,"$A$",dx=.12,dy=.1); _point(ax,b,"$B$",dx=-.45,dy=.12)
    ax.text(-.1,2.6,r"球內弦長 $4\sqrt{3}$",color=F.BLUE,ha="center")
    ax.text(-2.6,4.0,"球面最短路徑 $8\\pi/3$",color=F.RED)
    ax.set_xlim(-4.8,4.8); ax.set_ylim(-4.6,5.0); ax.axis("off")
    ax.set_title("球面上的最短路徑沿通過兩點與球心的大圓劣弧")
    fig.tight_layout()
    return _save(fig, "數B4-1-弦長與大圓弧長.svg")


def fig_conic_gallery():
    x=np.linspace(-3,3,800)
    fig,axes=plt.subplots(1,3,figsize=(12,4.1))
    y=0.45*x*x
    assert y.min()>=0 and math.isclose(y[np.argmin(abs(x))],0,abs_tol=3e-5)
    axes[0].plot(x,y,color=F.BLUE,lw=2.5); axes[0].set_title("拋物線 $y=0.45x^2$")
    t=np.linspace(0,2*math.pi,800); ex=3*np.cos(t); ey=1.7*np.sin(t)
    assert np.max(np.abs(ex*ex/9+ey*ey/(1.7**2)-1))<1e-10
    axes[1].plot(ex,ey,color=F.GREEN,lw=2.5); axes[1].set_title("橢圓 $x^2/9+y^2/2.89=1$")
    hx=np.linspace(2.05,4,400); hy=2*np.sqrt(hx*hx/4-1)
    assert np.max(np.abs(hx*hx/4-hy*hy/4-1))<1e-10
    axes[2].plot(hx,hy,color=F.RED,lw=2.5); axes[2].plot(hx,-hy,color=F.RED,lw=2.5); axes[2].plot(-hx,hy,color=F.RED,lw=2.5); axes[2].plot(-hx,-hy,color=F.RED,lw=2.5)
    axes[2].set_title("雙曲線 $x^2/4-y^2/4=1$")
    for ax in axes:
        ax.axhline(0,color=F.GRID,lw=1); ax.axvline(0,color=F.GRID,lw=1); ax.set_aspect("equal"); ax.set_xlim(-4.3,4.3); ax.set_ylim(-3.2,4.3); ax.grid(alpha=.15)
    fig.suptitle("三類圓錐曲線：開口、封閉與兩支",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-圓錐曲線方程圖.svg")


def fig_cone_cuts():
    alpha=30.; betas=[90.,55.,30.,15.]
    labels=["圓：$\\beta=90^\\circ$","橢圓：$\\alpha<\\beta<90^\\circ$","拋物線：$\\beta=\\alpha$","雙曲線：$\\beta<\\alpha$"]
    assert labels and betas[0]>betas[1]>betas[2]>betas[3]
    fig,axes=plt.subplots(2,2,figsize=(9.4,7.2))
    cone_h=3.; cone_x=cone_h*math.tan(math.radians(alpha))
    assert math.isclose(math.degrees(math.atan2(cone_x,cone_h)),alpha)
    for ax,beta,label in zip(axes.ravel(),betas,labels):
        ax.plot([-cone_x,0,cone_x],[-cone_h,0,-cone_h],color=F.INK,lw=1.8)
        ax.plot([-cone_x,0,cone_x],[cone_h,0,cone_h],color=F.INK,lw=1.8)
        angle=math.radians(90-beta); center=np.array([0.,1.0]); direction=np.array([math.cos(angle),math.sin(angle)])
        measured=math.degrees(math.acos(abs(np.dot(direction,np.array([0.,1.])))))
        assert math.isclose(measured,beta,abs_tol=1e-10)
        p=center-3.5*direction; q=center+3.5*direction
        ax.plot([p[0],q[0]],[p[1],q[1]],color=F.RED,lw=2.5)
        ax.plot([0,0],[-3.4,3.4],color=F.BLUE,ls="--",lw=1.2)
        ax.text(.2,2.65,"軸 $L$",color=F.BLUE); ax.set_xlim(-3,3); ax.set_ylim(-3.5,3.5); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(label,fontsize=10.5)
    fig.suptitle("截平面與軸的銳夾角 $\\beta$ 和圓錐半頂角 $\\alpha$ 比較",fontsize=15)
    fig.tight_layout(rect=(0,0,1,.94))
    return _save(fig, "數B4-1-圓錐截痕分類.svg")


def fig_degenerate_cuts():
    fig,axes=plt.subplots(1,3,figsize=(10.5,3.9))
    data=[("一點",[(0,0)],F.BLUE),("一直線",[(-2,-2),(2,2)],F.GREEN),("兩相交直線",[(-2,-2),(2,2),(-2,2),(2,-2)],F.RED)]
    for ax,(title,pts,color) in zip(axes,data):
        if len(pts)==1: _point(ax,pts[0],"$K$",color=color,dx=.12,dy=.12,size=55)
        elif len(pts)==2: ax.plot([pts[0][0],pts[1][0]],[pts[0][1],pts[1][1]],color=color,lw=3); _point(ax,(0,0),"$K$",dx=.12,dy=.12)
        else:
            ax.plot([-2,2],[-2,2],color=color,lw=3); ax.plot([-2,2],[2,-2],color=color,lw=3); _point(ax,(0,0),"$K$",dx=.12,dy=.12)
        ax.set_xlim(-2.5,2.5); ax.set_ylim(-2.5,2.5); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title)
    fig.suptitle("截平面通過圓錐頂點 $K$ 時的退化截痕",fontsize=15)
    fig.tight_layout()
    return _save(fig, "數B4-1-退化圓錐截痕.svg")


def fig_parabola_focus():
    f=.8; x=np.linspace(-3.2,3.2,500); y=x*x/(4*f)
    focus=np.array([0.,f]); directrix=-f
    tests=np.array([-2.4,-1.0,.6,2.2])
    for xx in tests:
        yy=xx*xx/(4*f)
        assert math.isclose(math.hypot(xx,yy-f),yy-directrix,rel_tol=1e-12)
    fig,ax=F.canvas(8.8,5.8,equal=True)
    ax.plot(x,y,color=F.BLUE,lw=2.6); ax.axhline(directrix,color=F.GREEN,ls="--",lw=1.8)
    _point(ax,focus,"$F$",color=F.RED,dx=.12,dy=.12,size=45)
    p=np.array([1.6,1.6**2/(4*f)])
    ax.plot([p[0],focus[0]],[p[1],focus[1]],color=F.RED,lw=2)
    ax.plot([p[0],p[0]],[p[1],directrix],color=F.GREEN,lw=2)
    _point(ax,p,"$P$",dx=.12,dy=.12)
    tangent=np.array([1.,p[0]/(2*f)]); normal=np.array([-tangent[1],1.]); normal=normal/np.linalg.norm(normal)
    incoming=np.array([0.,-1.]); reflected=np.array([focus[0]-p[0],focus[1]-p[1]]); reflected/=np.linalg.norm(reflected)
    assert math.isclose(abs(np.dot(incoming,normal)),abs(np.dot(reflected,normal)),rel_tol=1e-9)
    F.arrow(ax,(p[0],4.6),p,color=F.AMBER); F.arrow(ax,p,focus,color=F.RED)
    ax.text(-3.1,directrix-.38,"準線",color=F.GREEN); ax.text(1.9,3.85,"平行入射",color=F.AMBER)
    ax.text(-3.3,4.45,"$PF=$ 點到準線的距離",fontsize=12)
    ax.set_xlim(-3.7,3.8); ax.set_ylim(-1.35,5.0); ax.axis("off")
    ax.set_title("拋物線把平行於軸的訊號集中到焦點")
    fig.tight_layout()
    return _save(fig, "數B4-1-拋物線反射.svg")


def fig_ellipse_reflection():
    a,b=4.,2.5; c=math.sqrt(a*a-b*b); f1=np.array([-c,0.]); f2=np.array([c,0.])
    t=np.linspace(0,2*math.pi,600); x=a*np.cos(t); y=b*np.sin(t)
    sums=np.hypot(x+c,y)+np.hypot(x-c,y)
    assert np.max(np.abs(sums-2*a))<1e-10
    p=np.array([a*math.cos(.95),b*math.sin(.95)])
    fig,ax=F.canvas(9.6,5.2,equal=True)
    ax.plot(x,y,color=F.BLUE,lw=2.6)
    _point(ax,f1,"$F_1$",color=F.RED,dx=-.5,dy=.15,size=42); _point(ax,f2,"$F_2$",color=F.RED,dx=.12,dy=.15,size=42); _point(ax,p,"$P$",dx=.12,dy=.12)
    F.arrow(ax,f1,p,color=F.AMBER); F.arrow(ax,p,f2,color=F.GREEN)
    ax.text(-1.5,2.85,"$PF_1+PF_2=2a=8$",fontsize=12)
    ax.text(-3.1,1.45,"入射",color=F.AMBER); ax.text(2.0,1.3,"反射",color=F.GREEN)
    ax.set_xlim(-4.7,4.7); ax.set_ylim(-3.1,3.4); ax.axis("off")
    ax.set_title("橢圓邊界把一個焦點發出的訊號反射到另一焦點")
    fig.tight_layout()
    return _save(fig, "數B4-1-橢圓焦點反射.svg")


def main():
    outputs=[]
    for entrypoint, filename in FIGURE_OUTPUTS:
        function=globals().get(entrypoint)
        if not callable(function):
            raise AssertionError(f"找不到圖形函式：{entrypoint}")
        produced=function()
        expected=os.path.join(CHAPTER,"assets",filename)
        if os.path.abspath(produced)!=os.path.abspath(expected):
            raise AssertionError(f"{entrypoint} 輸出與 FIGURE_OUTPUTS 不一致")
        if not os.path.exists(expected):
            raise AssertionError(f"未產生：{expected}")
        outputs.append(expected)
    if len(set(outputs))!=len(FIGURE_OUTPUTS):
        raise AssertionError("FIGURE_OUTPUTS 含重複輸出")
    print(f"generated {len(outputs)} SVG files")


if __name__ == "__main__":
    main()
