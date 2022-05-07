# Covid 19 epidemic simulation
### Team Member(s):
kentchen831213, cklynn, tessachang

## Description


## Coding descript

For hypotheses 1,2 and 4, we combine them into one python script(bouncing_ball.py) in the hypothesis_1_2_4 folder. Users can set which hypothesis they want to test and set the number of corresponding parameters on the top of the script. For example, for hypothesis1, users can set the RATE_VACCINE to see the different coverage of vaccines how to influence epidemic transmission. For hypothesis2, users can set RATE_MASK to see the relationship between the coverage rate of masks and epidemic transmission rate. Lastly, users can set different numbers of DECREASE_RATE to test the hypothesis4. 

### hypothesis1 Assume wearing a facemask is mandated, a sweet spot for vaccination coverage rate exists
In hypothesis 1, we configure the simulation with following settings:
100% peoeple wearing surgical mask(66% protection rate), taken pfizer vaccine(0.66 protection rate) and assume the prevalent virus variant to be Omicron.
We discovered the sweet spot for vaccination rate exists around 80% by running 100 simulations per vaccine coverage rate.

| Vaccination rate | Healthy(%) | Infected(%) |
| -----------------| ------- | ---------|
| 0.5 | 31.6 | 70.4 |
| 0.6 | 33.7 | 68.3 |
| 0.7 | 49.6 | 52.4 |
| 0.8 | 74.7 | 27.3 |
| 0.8 | 62.25 | 39.75 |

### hypothesis2 Assume a fixed infection rate and the vaccination coverage rate, the minimum number ratio for the population to wear a mask
To verify hypothesis 2. We use an extreme set of configuration to minimize the randomness from mask types. We asuume everyone wearing a N95 mask with 83% pertection against the virus and no vaccination are available. But the result only showed that the more people weraing the mask the less likely the virus will spread.

| Mask-wearing rate | Healthy(%) | Infected(%) |
| ----------------- | ---------- | ----------- |
| 0.7 | 17.6 | 84.4 |
| 0.75 | 18.25 | 83.75 |
| 0.8 | 16.8 | 85.2 |
| 0.85 | 18.6 | 83.4 |
| 0.9 | 20.9 | 81.1 |
| 0.95 | 37.1 | 63.9 |

### hypothesis3 Travel bans help mitigate the spread of infection

### hypothesis4 will vaccine effectiveness degradation affect curve-flattening?

For hypothesis4, we want to check Will vaccine effectiveness degradation affects curve-flattening?

We set the Mask Wearing Rate: 1.0(everyone has taking mask), Mask Protection Rate: 0.66, Vaccine Coverage Rate: 0.5, and Vaccine Protection Rate:0.72. 
We decrease the vaccine protection rate each 5 seconds for 20%, 30%, 40%, 50%, and 60%. By comparing different decrease levels, we want to check whether vaccine degradation affects the infected curve, and the following is our experiment result:

| Decrease rate5/5seconds | Healthy(%) | Infected(%) | Number of people infected per second |
| --- | ----------- |  ----------- |  ----------- |
|0.2 | 12.61 | 89.39 | 1.91 | 
|0.3 | 12.42 | 89.58 | 2.38 | 
|0.4 | 12.16 | 89.84 | 3.46 | 
|0.5 | 11.63 | 90.36 | 3.57 | 
|0.6 | 10.54 | 91.46 | 3.74 | 


![image](https://user-images.githubusercontent.com/32189071/167099676-94ece0b8-7e27-41c8-9ae6-d98114825ccd.png)

![image](https://user-images.githubusercontent.com/32189071/167100013-a855dfb6-7362-49a8-bfb0-c730edc47274.png)

![image](https://user-images.githubusercontent.com/32189071/167100265-45803e41-8da9-4e96-bd7d-e1bc884c664b.png)

![image](https://user-images.githubusercontent.com/32189071/167100411-d670b4e9-3641-4894-aa67-8546bf4d38a2.png)

![image](https://user-images.githubusercontent.com/32189071/167100571-1335336f-06e2-4551-86b7-902da908ce7b.png)

According to our analysis result, the sloop of infected people is bigger with the degradation rate increase. Therefore, we can not reject the hypothesis, the vaccine effectiveness would influence the curve. 

