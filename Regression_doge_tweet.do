* AR ~ AS, OLS/heteroskedasticity
reg ar_price ar_sent if timestamp==0, vce(robust)

* AR ~ AS, FGLS
regress ar_price ar_sent if timestamp==0
predict e, resid
gen e2 = e^2
regress e2 ar_sent if timestamp==0
predict var, xb
gen w = 1/sqrt(var)
regress ar_price ar_sent [aweight=w] if timestamp==0

* AR ~ AS, OLS/heteroskedasticity without outlier
reg ar_price ar_sent if timestamp==0 & event_id!=17, vce(robust)

* AR ~ AS, FGLS without outlier
regress ar_price ar_sent if timestamp==0 & event_id!=17
predict e, resid
gen e2 = e^2
regress e2 ar_sent if timestamp==0 & event_id!=17
predict var, xb
gen w = 1/sqrt(var)
regress ar_price ar_sent [aweight=w] if timestamp==0 & event_id!=17

* 정규성 검토(이상치 제거)
swilk ar_sent if timestamp==0 & event_id!=17
swilk ar_price if timestamp==0 & event_id!=17

*이분산성 검토(이상치 제거)
reg ar_price ar_sent if timestamp==0 & event_id!=17
hettest

* pearson 상관분석
pwcorr ar_price ar_sent if timestamp==0 & event_id!=17, sig

* kendall's tau 상관분석
ktau ar_price ar_sent if timestamp==0 & event_id!=17

*AR~CAS(회귀 및 산포도)
reg ar_price_lag1 car_sent if timestamp==1 & event_id!=17, vce(robust)
scatter ar_price_lag1 car_sent if timestamp==1 & event_id!=17