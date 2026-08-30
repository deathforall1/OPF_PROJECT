import numpy as np
from style import *
from model import UltraTech, Ambuja, grid
u = UltraTech(); R = u.run(); Y = u.years
a = Ambuja(); RA = a.run()

H = dict(  # ten-year standalone history, as published
 yr=["FY17","FY18","FY19","FY20","FY21","FY22","FY23","FY24","FY25","FY26"],
 vol=[48.87,59.33,80.78,77.46,81.25,88.02,100.06,112.81,125.81,140.75],
 rev=[23891,29358,39999,40649,43188,50663,61237,68641,71895,82170],
 ebitda=[4969,5883,7079,8652,10965,10936,10286,12620,12296,15439],
 ebit=[4361,4719,5255,6924,9319,9091,8018,10255,9250,11761],
 real=[4888.68,4948.26,4951.60,5247.74,5315.45,5755.85,6120.03,6084.66,5714.57,5838.01],
 ic=[23546,40354,49969,49676,46974,50986,59937,65294,81733,86090],
 nd=[-2423,12008,17413,13293,4733,4661,3457,1994,16857,15462],
 nw=[23941,25923,33297,38296,43353,49271,53408,59095,69678,74663])

# U1 football field
def f_football():
    fig, ax = newfig(3.35, 1.95)
    _g=grid(u,R,[.10,.12],[u.g]); _lo,_hi=sorted([_g[0][0],_g[1][0]])
    rows=[("DCF, five methods\n(all reconcile)","","",BLUE,R["vps"],R["vps"]),
          ("DCF range, WACC 10-12%\nat g 6.99%","","",BLUE,_lo,_hi),
          ("Sell-side operating case\nrun through this DCF","","",AQUA,6130,6130),
          ("Peer median EV/EBITDA\n(19.05x)","","",ORANGE,9667,9667),
          ("Peer median P/E (54.2x)","","",ORANGE,14264,14264)]
    for i,(lab,_,_,c,lo,hi) in enumerate(rows):
        y=len(rows)-1-i
        if hi-lo<1:
            ax.plot([lo],[y],"D",color=c,ms=6,zorder=4)
            ax.text(lo+380,y,f"{lo:,.0f}",va="center",fontsize=6.7,color=INK,fontweight="bold")
        else:
            ax.barh(y,hi-lo,left=lo,height=.42,color=c,alpha=.85,zorder=3)
            ax.text(hi+380,y,f"{lo:,.0f}-{hi:,.0f}",va="center",fontsize=6.5,color=INK)
    ax.axvline(u.price,color=BAD,lw=1.5,zorder=5)
    ax.text(u.price+430,1.50,f"Traded\nRs {u.price:,.0f}",color=BAD,fontsize=6.8,
            fontweight="bold",va="center")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows][::-1],fontsize=6.5)
    ax.set_xlim(0,19800); ax.set_xlabel("Value per share (Rs)")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.set_title("Exhibit U1  Football field: the DCF sits far below every alternative")
    tidy(ax,ygrid=False,xgrid=True); save(fig,"utcl_football")

# U2 bridge
def f_bridge():
    fig, ax = newfig(3.35, 2.25)
    waterfall(ax,["EV of\noperations","+ Liquid\ninvestments","+ Subsidiary\nholdings",
                  "- Loan\nfunds","- Lease\nliabilities","- Minority\ninterest"],
              [u.liquid,u.inv,-u.loans,-u.leases,-u.nci],
              start=R["ev"],total_label="Equity\nvalue")
    ax.set_ylabel("Rs crore"); ax.set_ylim(0,R["ev"]*1.18)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.set_title("Exhibit U2  From enterprise value to equity")
    save(fig,"utcl_bridge")

# U3 FCFF
def f_fcff():
    fig, ax = newfig(3.35,1.85)
    ax.bar(Y,R["fcff"],color=BLUE,width=.6,zorder=3)
    bar_labels(ax,Y,R["fcff"],"{:,.0f}",dy=.025)
    ax.set_ylabel("FCFF (Rs cr)")
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.set_ylim(0,16800)
    ax.set_title("Exhibit U3  Free cash flow is positive throughout")
    tidy(ax); save(fig,"utcl_fcff")

# U4 ROIC history + forecast  (after-tax, recomputed)
def f_roic():
    fig, ax = newfig(3.35,2.05)
    hist=[H["ebit"][i]*(1-u.tax)/H["ic"][i-1]*100 for i in range(1,10)]
    xh=np.arange(len(hist)); xf=np.arange(len(hist),len(hist)+len(Y))
    ax.plot(xh,hist,"-o",color=MUTED,lw=1.6,ms=3.0,label="Realised (after tax)")
    ax.plot([xh[-1],xf[0]],[hist[-1],R["roic"][0]*100],color=GRID,lw=1.2)
    ax.plot(xf,np.array(R["roic"])*100,"-o",color=BLUE,lw=1.9,ms=3.4,label="Forecast")
    ax.axhline(u.wacc*100,color=BAD,lw=1.4,ls="--")
    ax.text(0.1,u.wacc*100+.30,f"WACC {u.wacc*100:.2f}%",color=BAD,fontsize=6.6,fontweight="bold")
    ax.annotate(f"{R['roic'][-1]*100:.1f}%",(xf[-1],R["roic"][-1]*100),
                textcoords="offset points",xytext=(-3,5),fontsize=6.7,color=BLUE,
                ha="right",fontweight="bold")
    ax.annotate("10.8%",(xh[-1],hist[-1]),textcoords="offset points",xytext=(-4,-10),
                fontsize=6.5,color=MUTED,ha="right")
    labs=H["yr"][1:]+Y
    ax.set_xticks(list(xh)+list(xf)); ax.set_xticklabels(labs,rotation=55,fontsize=6.0)
    ax.set_ylabel("ROIC (%)"); ax.set_ylim(8,17.5)
    ax.legend(fontsize=6.3,loc="lower right")
    ax.set_title("Exhibit U4  A falling return, forecast to reverse")
    tidy(ax); save(fig,"utcl_roic")

# U5 EVA
def f_eva():
    fig, ax = newfig(3.35,1.85)
    ax.bar(Y,R["eva"],color=GOOD,width=.6,zorder=3)
    bar_labels(ax,Y,R["eva"],"{:,.0f}",dy=.025)
    ax.set_ylabel("EVA (Rs cr)"); ax.set_ylim(0,5100)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.set_title("Exhibit U5  UltraTech does create economic value")
    tidy(ax); save(fig,"utcl_eva")

# U6 volume vs realisation - two panels, never a dual axis
def f_hist():
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(3.35,2.6),sharex=True)
    x=np.arange(10)
    ax1.bar(x,H["vol"],color=BLUE,width=.62,zorder=3)
    ax1.set_ylabel("Volume (Mn.T)")
    ax1.text(0.2,128,"CAGR 12.5%",fontsize=6.6,color=BLUE,fontweight="bold")
    ax1.set_title("Exhibit U6  Volume compounded; price did not")
    tidy(ax1)
    ax2.plot(x,H["real"],"-o",color=ORANGE,lw=1.8,ms=3.2)
    ax2.set_ylabel("Realisation\n(Rs/tonne)"); ax2.set_ylim(4600,6500)
    ax2.text(0.2,6250,"CAGR 2.0%",fontsize=6.6,color=ORANGE,fontweight="bold")
    ax2.annotate("-6.1% in FY25",(8,H["real"][8]),textcoords="offset points",
                 xytext=(-6,-13),fontsize=6.2,color=BAD,ha="right")
    ax2.set_xticks(x); ax2.set_xticklabels(H["yr"],rotation=50,fontsize=6.2); tidy(ax2)
    save(fig,"utcl_hist")

# U7 revenue and margin - separate panels
def f_revmarg():
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(3.35,2.6),sharex=True)
    x=np.arange(10)
    ax1.bar(x,H["rev"],color=BLUE,width=.62,zorder=3)
    ax1.set_ylabel("Revenue (Rs cr)")
    ax1.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax1.set_title("Exhibit U7  Revenue grew 14.7% a year; margin did not follow")
    tidy(ax1)
    marg=[H["ebitda"][i]/H["rev"][i]*100 for i in range(10)]
    ax2.plot(x,marg,"-o",color=ORANGE,lw=1.8,ms=3.2)
    ax2.set_ylabel("EBITDA margin (%)"); ax2.set_ylim(15,27)
    ax2.annotate("FY21 fuel windfall 25.4%",(4,marg[4]),textcoords="offset points",
                 xytext=(4,4),fontsize=6.1,color=MUTED)
    ax2.set_xticks(x); ax2.set_xticklabels(H["yr"],rotation=50,fontsize=6.2); tidy(ax2)
    save(fig,"utcl_revmarg")

# U8 corrected sensitivity
def f_sens():
    fig,ax=newfig(3.35,1.95)
    ws=[.095,.105,.1143,.125,.135]; gs=[.04,.05,.06,.065,.07]
    M=grid(u,R,ws,gs)
    heat(ax,M,[f"{w*100:.2f}%" for w in ws],[f"{g*100:.1f}%" for g in gs],
         fmt="{:,.0f}",ref=(2,4),title_x="Terminal growth",title_y="WACC")
    ax.set_title("Exhibit U8  Rebuilt grid: no cell reaches Rs 10,745")
    save(fig,"utcl_sens")

# U9 peers
def f_peers():
    fig,ax=newfig(3.35,1.85)
    names=["Ambuja\n(consol.)","Ramco","Shree","JK Cement","UltraTech"]
    vals=[17.00,18.98,19.05,19.69,21.06]
    cols=[MUTED]*4+[BLUE]
    ax.bar(names,vals,color=cols,width=.6,zorder=3)
    bar_labels(ax,names,vals,"{:.1f}x",dy=.02)
    ax.axhline(19.05,color=ORANGE,ls="--",lw=1.2)
    ax.text(2.0,21.6,"Peer median 19.05x",fontsize=6.3,color=ORANGE,ha="center")
    ax.set_ylabel("EV / EBITDA (x)"); ax.set_ylim(0,23.5)
    ax.set_title("Exhibit U9  The most expensive name in the set")
    tidy(ax); save(fig,"utcl_peers")

# U10 EBITDA per tonne: the acquisition drag
def f_pertonne():
    fig,ax=newfig(3.35,1.8)
    n=["Core UltraTech\nassets","Kesoram","India Cements"]; v=[966,755,386]
    ax.barh(range(3),v,color=[BLUE,WARN,BAD],height=.5,zorder=3)
    for i,val in enumerate(v):
        ax.text(val+18,i,f"Rs {val}",va="center",fontsize=6.9,color=INK,fontweight="bold")
    ax.set_yticks(range(3)); ax.set_yticklabels(n,fontsize=6.6)
    ax.invert_yaxis(); ax.set_xlim(0,1180); ax.set_xlabel("EBITDA per tonne (Rs)")
    ax.set_title("Exhibit U10  What the acquisitions actually earn")
    tidy(ax,ygrid=False,xgrid=True); save(fig,"utcl_pertonne")

# U11 capacity / utilisation
def f_capacity():
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(3.35,2.5),sharex=True,
                               gridspec_kw={"height_ratios":[1.35,1]})
    x=np.arange(len(Y))
    ax1.bar(x,u.capacity,color="#d7e3f5",width=.6,zorder=2,label="Capacity")
    ax1.bar(x,R["vol"],color=BLUE,width=.38,zorder=3,label="Volume sold")
    ax1.set_ylabel("Mn tonnes"); ax1.legend(fontsize=6.3,ncol=2,loc="upper left")
    ax1.set_ylim(0,252)
    ax1.set_title("Exhibit U11  Growth comes from filling plants already built")
    tidy(ax1)
    ax2.plot(x,np.array(u.util)*100,"-o",color=ORANGE,lw=1.8,ms=3.2)
    ax2.set_ylabel("Utilisation (%)"); ax2.set_ylim(79,89)
    ax2.annotate("86%",(x[-1],86),textcoords="offset points",xytext=(-3,4),
                 fontsize=6.6,color=ORANGE,ha="right")
    ax2.set_xticks(x); ax2.set_xticklabels(Y,rotation=45); tidy(ax2)
    save(fig,"utcl_capacity")

# U12 net debt history
def f_netdebt():
    fig,ax=newfig(3.35,1.75)
    x=np.arange(10)
    cols=[GOOD if v<0 else BLUE for v in H["nd"]]
    ax.bar(x,H["nd"],color=cols,width=.62,zorder=3)
    ax.set_xticks(x); ax.set_xticklabels(H["yr"],rotation=50,fontsize=6.2)
    ax.set_ylabel("Net debt (Rs cr)"); ax.set_ylim(-5000,21500)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.annotate("India Cements &\nKesoram acquired",(8,H["nd"][8]),
                textcoords="offset points",xytext=(-52,-24),fontsize=6.1,color=INK2,
                arrowprops=dict(arrowstyle="->",color=MUTED,lw=.7))
    ax.set_title("Exhibit U12  Leverage returns with the acquisitions")
    tidy(ax,zero=True); save(fig,"utcl_netdebt")

# U13 terminal value share
def f_tv():
    fig,ax=newfig(3.35,1.62)
    for i,(nm,pe,pt,ev) in enumerate([("UltraTech\n5-yr horizon",R["pv"],R["pvtv"],R["ev"]),
                                      ("Ambuja\n10-yr horizon",RA["pv"],RA["pvtv"],RA["ev"])]):
        ax.barh(i,pe/ev*100,color=BLUE,height=.42,zorder=3)
        ax.barh(i,pt/ev*100,left=pe/ev*100,color=ORANGE,height=.42,zorder=3)
        ax.text(pe/ev*50,i,f"{pe/ev*100:.0f}%",ha="center",va="center",color="white",
                fontsize=7,fontweight="bold")
        ax.text(pe/ev*100+pt/ev*50,i,f"{pt/ev*100:.0f}%",ha="center",va="center",
                color="white",fontsize=7,fontweight="bold")
    ax.set_yticks([0,1]); ax.set_yticklabels(["UltraTech\n5-yr horizon","Ambuja\n10-yr horizon"],fontsize=6.5)
    ax.invert_yaxis(); ax.set_xlim(0,100); ax.set_xlabel("Share of enterprise value (%)")
    ax.text(14,-.70,"PV of explicit FCFF",fontsize=6.2,color=BLUE,fontweight="bold")
    ax.text(58,-.70,"PV of terminal value",fontsize=6.2,color=ORANGE,fontweight="bold")
    ax.set_ylim(1.62,-1.05)
    ax.set_title("Exhibit U13  Horizon length decides terminal dominance")
    tidy(ax,ygrid=False,xgrid=True); save(fig,"utcl_tv")

# U14 capex vs depreciation
def f_capex():
    fig,ax=newfig(3.35,1.8)
    x=np.arange(len(Y)); w=.36
    ax.bar(x-w/2,u.capex,w,color=BLUE,zorder=3,label="Capex")
    ax.bar(x+w/2,R["dep"],w,color=MUTED,zorder=3,label="Depreciation")
    ax.set_xticks(x); ax.set_xticklabels(Y,rotation=45)
    ax.set_ylabel("Rs crore"); ax.legend(fontsize=6.3,ncol=2,loc="upper right")
    ax.set_ylim(0,12800)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f"{v:,.0f}"))
    ax.set_title("Exhibit U14  Capex above depreciation throughout")
    tidy(ax); save(fig,"utcl_capex")

for f in [f_football,f_bridge,f_fcff,f_roic,f_eva,f_hist,f_revmarg,f_sens,
          f_peers,f_pertonne,f_capacity,f_netdebt,f_tv,f_capex]:
    f(); print("ok",f.__name__)
