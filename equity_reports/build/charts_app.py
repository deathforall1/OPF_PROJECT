import numpy as np
from style import *
from model import Ambuja, UltraTech
a=Ambuja(); RA=a.run(); u=UltraTech(); RU=u.run()

# C1 both ROIC paths vs their WACC
def f_roic():
    fig,ax=newfig(3.35,2.0)
    xa=np.arange(10); xu=np.arange(5)
    ax.plot(xa,np.array(RA["roic_g"])*100,"-o",color=ORANGE,lw=1.8,ms=3.2,
            label="Ambuja (incl. goodwill)")
    ax.plot(xa,np.array(RA["roic_o"])*100,"--",color=ORANGE,lw=1.3,alpha=.75,
            label="Ambuja (operating only)")
    ax.plot(xu,np.array(RU["roic"])*100,"-o",color=BLUE,lw=1.9,ms=3.4,
            label="UltraTech")
    ax.axhline(a.wacc*100,color=BAD,lw=1.2,ls=":")
    ax.text(9.85,a.wacc*100+.22,"WACC ~11.3%",color=BAD,fontsize=6.4,ha="right",
            fontweight="bold")
    ax.set_xticks(xa); ax.set_xticklabels([f"Yr {i+1}" for i in range(10)],fontsize=6.2,rotation=45)
    ax.set_ylabel("ROIC (%)"); ax.set_ylim(2,17.5); ax.legend(fontsize=6.2,loc="upper left")
    ax.set_title("Exhibit C1  Both forecasts assume returns improve")
    tidy(ax); save(fig,"app_roic")

# C2 EV/IC justified vs actual
def f_evic():
    fig,ax=newfig(3.35,1.95)
    labs=["Justified on\ntoday's ROIC","Justified on\nterminal ROIC","Actual, at the\ntraded price"]
    gA,gU=a.g,u.g
    # actual EV/IC at the traded price, invested capital INCLUDING goodwill for both
    evic_u=(u.mcap+u.loans+u.leases+u.nci-u.liquid-u.inv)/(RU["ic_o"][0]+u.gw)
    evic_a=(a.mcap+a.debt+a.nci-a.cash)/(RA["ic_o"][0]+a.gw)
    ut=[(0.108-gU)/(u.wacc-gU),(RU["t_roic"]-gU)/(u.wacc-gU),evic_u]
    am=[(0.033-gA)/(a.wacc-gA),(RA["t_roic"]-gA)/(a.wacc-gA),evic_a]
    x=np.arange(3); w=.36
    ax.bar(x-w/2,ut,w,color=BLUE,zorder=3,label="UltraTech")
    ax.bar(x+w/2,am,w,color=ORANGE,zorder=3,label="Ambuja")
    for xi,v in zip(x-w/2,ut):
        ax.text(xi,v+.10,f"{v:.2f}x",ha="center",fontsize=6.4,color=INK)
    for xi,v in zip(x+w/2,am):
        ax.text(xi,v+(.10 if v>=0 else -.10),f"{v:.2f}x",ha="center",
                va="bottom" if v>=0 else "top",fontsize=6.4,color=INK)
    ax.set_xticks(x); ax.set_xticklabels(labs,fontsize=6.4)
    ax.set_ylabel("EV / invested capital (x)"); ax.set_ylim(-1.5,4.6)
    ax.legend(fontsize=6.4,ncol=2,loc="upper left")
    ax.set_title("Exhibit C2  What the price pays vs what the return justifies")
    tidy(ax,zero=True); save(fig,"app_evic")

# C3 goodwill intensity
def f_gw():
    fig,ax=newfig(3.35,1.62)
    nm=["Ambuja","UltraTech"]; gw=[34.2,8.9]
    ax.barh(range(2),gw,color=[ORANGE,BLUE],height=.44,zorder=3)
    for i,v in enumerate(gw):
        ax.text(v+0.8,i,f"{v:.1f}%",va="center",fontsize=7.4,color=INK,fontweight="bold")
    ax.set_yticks(range(2)); ax.set_yticklabels(nm,fontsize=7.2); ax.invert_yaxis()
    ax.set_xlim(0,42); ax.set_xlabel("Goodwill & intangibles, % of invested capital")
    ax.set_title("Exhibit C3  How much of the capital base was bought")
    tidy(ax,ygrid=False,xgrid=True); save(fig,"app_gw")

# C4 upside/downside
def f_gap():
    fig,ax=newfig(3.35,1.72)
    nm=["Ambuja","UltraTech"]
    dcf=[RA["vps"],RU["vps"]]; mkt=[400.90,10745.0]
    gap=[(d/m-1)*100 for d,m in zip(dcf,mkt)]
    ax.barh(range(2),gap,color=BAD,height=.44,zorder=3)
    for i,(g,d,m) in enumerate(zip(gap,dcf,mkt)):
        ax.text(g-1.4,i,f"{g:.0f}%",va="center",ha="right",fontsize=7.6,
                color="white",fontweight="bold")
        ax.text(1.5,i,f"Rs {d:,.0f} vs Rs {m:,.0f}",va="center",fontsize=6.6,color=INK2)
    ax.set_yticks(range(2)); ax.set_yticklabels(nm,fontsize=7.2); ax.invert_yaxis()
    ax.set_xlim(-85,52); ax.set_xlabel("DCF value against traded price (%)")
    ax.axvline(0,color=MUTED,lw=.9)
    ax.set_title("Exhibit C4  Both names screen expensive on cash flow")
    tidy(ax,ygrid=False,xgrid=True); save(fig,"app_gap")

# C5 implied vs peer multiple
def f_mult():
    fig,ax=newfig(3.35,1.85)
    cats=["Ambuja","UltraTech"]
    dcf=[RA["tv"]/(RA["ebitda"][-1]*(1+a.g)),RU["tv"]/(RU["ebitda"][-1]*(1+u.g))]
    traded=[17.00,21.06]; peer=[19.37,19.05]
    x=np.arange(2); w=.26
    ax.bar(x-w,dcf,w,color=BLUE,zorder=3,label="Implied by our DCF")
    ax.bar(x,traded,w,color=ORANGE,zorder=3,label="Traded today")
    ax.bar(x+w,peer,w,color=MUTED,zorder=3,label="Peer median")
    for xi,v in zip(x-w,dcf): ax.text(xi,v+.35,f"{v:.1f}x",ha="center",fontsize=6.3,color=INK)
    for xi,v in zip(x,traded): ax.text(xi,v+.35,f"{v:.1f}x",ha="center",fontsize=6.3,color=INK)
    for xi,v in zip(x+w,peer): ax.text(xi,v+.35,f"{v:.1f}x",ha="center",fontsize=6.3,color=INK)
    ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=7.2)
    ax.set_ylabel("EV / EBITDA (x)"); ax.set_ylim(0,25.5)
    ax.legend(fontsize=6.2,ncol=3,loc="upper left")
    ax.set_title("Exhibit C5  The multiplier-consistency gap, both names")
    tidy(ax); save(fig,"app_mult")

# C6 audit findings
def f_audit():
    fig,ax=newfig(3.35,1.85)
    cats=["PASS","PARTIAL","FAIL"]
    amb=[18,4,0]; utc=[14,6,2]
    x=np.arange(3); w=.36
    ax.bar(x-w/2,amb,w,color=ORANGE,zorder=3,label="Ambuja")
    ax.bar(x+w/2,utc,w,color=BLUE,zorder=3,label="UltraTech")
    for xi,v in zip(x-w/2,amb): ax.text(xi,v+.18,str(v),ha="center",fontsize=6.8,color=INK)
    for xi,v in zip(x+w/2,utc): ax.text(xi,v+.18,str(v),ha="center",fontsize=6.8,color=INK)
    ax.set_xticks(x); ax.set_xticklabels(cats,fontsize=7.2)
    ax.set_ylabel("Checks"); ax.set_ylim(0,21.5); ax.legend(fontsize=6.4,ncol=2)
    ax.set_title("Exhibit C6  Consistency and sanity checks, as recorded")
    tidy(ax); save(fig,"app_audit")

for f in [f_roic,f_evic,f_gw,f_gap,f_mult,f_audit]:
    f(); print("ok",f.__name__)
