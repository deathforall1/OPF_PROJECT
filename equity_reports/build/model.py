"""Independent re-computation of both valuation models, from the workbook inputs.
Used to (a) verify the workbooks and (b) drive every exhibit in the report."""

# ----------------------------------------------------------------- AMBUJA
class Ambuja:
    name="Ambuja Cements Ltd"; ticker="AMBUJACEM"
    price=400.90; mcap=99095.0; shares=247.18
    years=["FY27","FY28","FY29","FY30","FY31","FY32","FY33","FY34","FY35","FY36"]
    capacity=[112,116,119,121,123,125,127,129,131,133]
    util=[.700,.725,.750,.775,.795,.810,.825,.835,.845,.850]
    real_g=[.048,.040,.032,.024,.020,.016,.014,.012,.012,.012]
    sa_share=[.615,.613,.611,.609,.607,.605,.604,.603,.602,.600]
    sa_marg=[.130,.142,.152,.160,.167,.173,.178,.183,.187,.190]
    sub_marg=[.236,.240,.244,.247,.250,.252,.254,.256,.258,.260]
    capex=[9500,9000,8500,8000,7500,7500,7500,7500,7500,7500]
    dep_rate=[.08]*10
    nwc_pct=[-.0034]*10
    # opening
    r0=5494.01; ofa0=44368.9; nwc0=-139.4; gw=22978.6
    tax=.25168; g=.06994
    beta_u=.90; de=.008738; dv=.00866268; kd=.08; rf=.0498; erp=.0708
    ke_ar=.114216917099405; wacc_ar=.113746088786624; rho_ar=.113920506741639
    cash=958.6; debt=865.93; protest=614.1; dtl=3466.33; nci=12498.9
    # base year actuals
    base_rev=40655.7; base_ebitda=6558.99; base_vol=74.0; base_ebitda_t=886.35

    def run(self):
        n=len(self.years); r=[];vol=[];rev=[];ebitda=[];dep=[];ebit=[];nopat=[]
        ofa_o=[];ofa_c=[];nwc=[];dnwc=[];fcff=[];ic_o=[];roic_g=[];roic_o=[]
        prev_r=self.r0; prev_ofa=self.ofa0; prev_nwc=self.nwc0
        for i in range(n):
            ri=prev_r*(1+self.real_g[i]); r.append(ri)
            v=self.capacity[i]*self.util[i]; vol.append(v)
            rv=v*ri/10; rev.append(rv)
            sa_rev=rv*self.sa_share[i]; sub_rev=rv-sa_rev
            eb=sa_rev*self.sa_marg[i]+sub_rev*self.sub_marg[i]; ebitda.append(eb)
            ofa_o.append(prev_ofa)
            d=prev_ofa*self.dep_rate[i]; dep.append(d)
            c=prev_ofa+self.capex[i]-d; ofa_c.append(c)
            e=eb-d; ebit.append(e); np_=e*(1-self.tax); nopat.append(np_)
            w=rv*self.nwc_pct[i]; nwc.append(w); dw=w-prev_nwc; dnwc.append(dw)
            fcff.append(np_+d-self.capex[i]-dw)
            ico=prev_ofa+prev_nwc; ic_o.append(ico)
            roic_o.append(np_/ico); roic_g.append(np_/(ico+self.gw))
            prev_r=ri; prev_ofa=c; prev_nwc=w
        ic_c=[ic_o[i]+ (self.capex[i]-dep[i]) + dnwc[i] for i in range(n)]
        # terminal
        t_nopat=nopat[-1]*(1+self.g); t_ic=ic_c[-1]
        t_reinv=self.g*t_ic; t_fcff=t_nopat-t_reinv
        t_roic=t_nopat/t_ic
        tv=t_fcff/(self.wacc-self.g)
        df=[1/(1+self.wacc)**(i+1) for i in range(n)]
        pv=sum(fcff[i]*df[i] for i in range(n))
        pvtv=tv*df[-1]; ev=pv+pvtv
        eq=ev+self.cash-self.debt+self.protest-self.dtl-self.nci
        vps=eq/self.shares
        # EVA
        cc=[ic_o[i]*self.wacc for i in range(n)]
        eva=[nopat[i]-cc[i] for i in range(n)]
        t_eva=t_nopat-t_ic*self.wacc
        eva_ev=ic_o[0]+sum(eva[i]*df[i] for i in range(n))+ (t_eva/(self.wacc-self.g))*df[-1]
        d=dict(locals()); d.pop('self'); return d

# --------------------------------------------------------------- ULTRATECH
class UltraTech:
    name="UltraTech Cement Ltd"; ticker="ULTRACEMCO"
    price=10745.0; mcap=316633.0; shares=29.468
    years=["FY27","FY28","FY29","FY30","FY31"]
    capacity=[186,195,205,213,220]
    util=[.820,.835,.845,.855,.860]
    ebt_g=[.08,.06,.04,.03,.025]
    sub_g=[.06,.055,.05,.045,.04]
    sub_marg=[.250,.252,.254,.256,.258]
    capex=[9500,9500,9000,8500,8500]
    dep_rate=[.050501]*5
    nwc_pct=[-.0374]*5
    ebt0=1096.91; r0=5838.36; ofa0=99626.8; nwc0=-5865.44; gw=7909.05
    sub_rev0=6341.88
    tax=.25168; g=.06994
    beta_u=.90; de=.064681; dv=.060751; kd=.0834; rf=.0498; erp=.0708
    ke_ar=.116604; wacc_ar=.113312; rho_ar=.114587
    liquid=1384.35; inv=6739.51; loans=22780.7; leases=974.43; nci=4088.9
    base_rev=82169.65; base_ebitda=15439.0; base_vol=140.75

    def run(self):
        n=len(self.years); ebt=[];r=[];vol=[];sa_rev=[];sa_eb=[];sub_rev=[];sub_eb=[]
        rev=[];ebitda=[];dep=[];ebit=[];nopat=[];ofa_o=[];ofa_c=[];nwc=[];dnwc=[];fcff=[]
        ic_o=[];roic=[]
        pe=self.ebt0; pr=self.r0; pofa=self.ofa0; pnwc=self.nwc0; psub=self.sub_rev0
        for i in range(n):
            e=pe*(1+self.ebt_g[i]); ebt.append(e)
            ri=pr*(1+self.ebt_g[i]*0.5); r.append(ri)
            v=self.capacity[i]*self.util[i]; vol.append(v)
            sr=v*ri/10; sa_rev.append(sr)
            se=v*e/10; sa_eb.append(se)
            ub=psub*(1+self.sub_g[i]); sub_rev.append(ub)
            ue=ub*self.sub_marg[i]; sub_eb.append(ue)
            rv=sr+ub; rev.append(rv); eb=se+ue; ebitda.append(eb)
            ofa_o.append(pofa); d=pofa*self.dep_rate[i]; dep.append(d)
            c=pofa+self.capex[i]-d; ofa_c.append(c)
            eo=eb-d; ebit.append(eo); np_=eo*(1-self.tax); nopat.append(np_)
            w=rv*self.nwc_pct[i]; nwc.append(w); dw=w-pnwc; dnwc.append(dw)
            fcff.append(np_+d-self.capex[i]-dw)
            ico=pofa+pnwc; ic_o.append(ico); roic.append(np_/ico)
            pe=e; pr=ri; pofa=c; pnwc=w; psub=ub
        ic_c=[ic_o[i]+(self.capex[i]-dep[i])+dnwc[i] for i in range(n)]
        t_nopat=nopat[-1]*(1+self.g); t_ic=ic_c[-1]
        t_reinv=self.g*t_ic; t_fcff=t_nopat-t_reinv; t_roic=t_nopat/t_ic
        tv=t_fcff/(self.wacc-self.g)
        df=[1/(1+self.wacc)**(i+1) for i in range(n)]
        pv=sum(fcff[i]*df[i] for i in range(n)); pvtv=tv*df[-1]; ev=pv+pvtv
        eq=ev+self.liquid+self.inv-self.loans-self.leases-self.nci
        vps=eq/self.shares
        cc=[ic_o[i]*self.wacc for i in range(n)]
        eva=[nopat[i]-cc[i] for i in range(n)]
        t_eva=t_nopat-t_ic*self.wacc
        eva_ev=ic_o[0]+sum(eva[i]*df[i] for i in range(n))+(t_eva/(self.wacc-self.g))*df[-1]
        d=dict(locals()); d.pop('self'); return d

def grid(co, res, waccs, gs):
    """Correct WACC x g sensitivity: value per share."""
    n=len(res['fcff']); out=[]
    for w in waccs:
        row=[]
        for g in gs:
            if g>=w-0.0005: row.append(None); continue
            df=[1/(1+w)**(i+1) for i in range(n)]
            tn=res['nopat'][-1]*(1+g); tf=tn-g*res['ic_c'][-1]
            ev=sum(res['fcff'][i]*df[i] for i in range(n))+tf/(w-g)*df[-1]
            if isinstance(co,Ambuja): eq=ev+co.cash-co.debt+co.protest-co.dtl-co.nci
            else: eq=ev+co.liquid+co.inv-co.loans-co.leases-co.nci
            row.append(eq/co.shares)
        out.append(row)
    return out


def _rates(cls):
    """Harris-Pringle Case 2 (constant D/V, continuous rebalancing), which is the
    debt policy both workbooks state. Relever carries no tax term."""
    cls.beta_l = cls.beta_u * (1 + cls.de)
    cls.ke  = cls.rf + cls.beta_l * cls.erp
    cls.wacc = (1 - cls.dv) * cls.ke + cls.dv * cls.kd * (1 - cls.tax)
    cls.rho  = (1 - cls.dv) * cls.ke + cls.dv * cls.kd
    return cls
_rates(Ambuja); _rates(UltraTech)
