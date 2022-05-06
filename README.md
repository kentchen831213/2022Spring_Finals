# Covid 19 epidemic simulation
### Description


### Coding descript

For hypotheses 1,2 and 4, we combine them into one python script(bouncing_ball.py) in the hypothesis_1_2_4 folder. Users can set which hypothesis they want to test and set the number of corresponding parameters on the top of the script. For example, for hypothesis1, users can set the RATE_VACCINE to see the different coverage of vaccines how to influence epidemic transmission. For hypothesis2, users can set RATE_MASK to see the relationship between the coverage rate of masks and epidemic transmission rate. Lastly, users can set different numbers of DECREASE_RATE to test the hypothesis4. 

### hypothesis1 Assume wearing a facemask is mandated, a sweet spot for vaccination coverage rate exists

### hypothesis2 Assume a fixed infection rate and the vaccination coverage rate, the minimum number ratio for the population to wear a mask

### hypothesis3 Travel bans help mitigate the spread of infection

### hypothesis4 Will vaccine effectiveness degradation affect curve-flattening?

For hypothesis4, we want to check Will vaccine effectiveness degradation affect curve-flattening?

We setting the Mask Wearing Rate: 1.0(everyone has taking mask), Mask Protection Rate: 0.66, Vaccine Coverage Rate: 0.5, and Vaccine Protection Rate:0.72. 
We decrease the vaccine protection rate each 5 seconds for 20%, 30%, 40%, 50%, and 60%. Through comparing different decrease level, we want to check whether vaccine degradtion affect infected curve, and the following is our experiment result:


the decrease rate of vaccine protection is 0.2
1.9165316880911802 person be infected every seconds
average healthy rate is 12.61
average infected rate is 89.39
![image](https://user-images.githubusercontent.com/32189071/167099676-94ece0b8-7e27-41c8-9ae6-d98114825ccd.png)

the decrease rate of vaccine protection is 0.3
2.3801410474073488 person be infected every seconds
average healthy rate is 12.42
average infected rate is 89.58
![image](https://user-images.githubusercontent.com/32189071/167100013-a855dfb6-7362-49a8-bfb0-c730edc47274.png)

the decrease rate of vaccine protection is 0.4
3.4670226616521598 person be infected every seconds
average healthy rate is 12.16
average infected rate is 89.84
![image](https://user-images.githubusercontent.com/32189071/167100265-45803e41-8da9-4e96-bd7d-e1bc884c664b.png)

the decrease rate of vaccine protection is 0.5
3.575632090389345 person be infected every seconds
average healthy rate is 11.63
average infected rate is 90.36
![image](https://user-images.githubusercontent.com/32189071/167100411-d670b4e9-3641-4894-aa67-8546bf4d38a2.png)

the decrease rate of vaccine protection is 0.6
3.745447062359358 person be infected every seconds
average healthy rate is 10.54
average infected rate is 91.46
![image](https://user-images.githubusercontent.com/32189071/167100571-1335336f-06e2-4551-86b7-902da908ce7b.png)

According to our analyzing result, the sloop of infected people bigger with the decrease rate increase. Therefore, we cannot reject the hypothesis, the vaccine effectiveness would influence the curve. 
