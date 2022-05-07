# Covid 19 epidemic simulation
### Description


### Coding descript

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








# 590PR Final Project

# Title: 
Monte Carlo Simulation of Air Ticket Overselling

## Team Member(s):
Cong Xiang, Chin-Han Lin, Xuefeng Qin

Xuefeng Qin created the main functions, inclusive of get_varaible, get_rev and Monte Carlo. The other parts are divided by Cong Xiang and Chin-Han Lin.

# Monte Carlo Simulation Scenario & Purpose:
Airline Companies usually oversell tickets to maximize the profits of each scheduled flight because there is a probability that some passengers who booked tickets will not take on the plane, overselling can raise the seat utilization. However, the exact number of overselling tickets is uncertain, which is very significant to be kept in a reasonable range. If overbooking numbers are not well controlled, it will lead to finance compensation and customer loss due to the absence of seats for excess passengers, or profit loss due to low seat utilization.

So in this model. we will simulate the real-world airline booking scenario based on Monte Carlo simulation principle to find out the best overbooking number range and purse the maximum profits for an airline company.

## Simulation's variables of uncertainty
We will take all the following variable into consideration, which are related to the profits of a single airline flight.
#### The demand of each class of a scheduled flight
The demand of a certain flight follows the binomial distribution in which the largest case numbers are 120% of the capacity, we randomly generate integers from this binomial distribution to represent the numbers of people who want to buy a ticket. Our decision is based on the reference.
#### The number of final show-up passengers 
The number of final show-up passengers also follows binominal distribution based on the reference, in which the largest case numbers are the number of sold tickets. Final show-up passenger number are randomly assigned from the binomial distribution we created.
#### The distribution of no-show passengers on different flight class (including business and economy)
In this model, we have considered two flight classes including the business and economy, and we will assign a total overbooking numbers of certain flight, overbooking tickets for two class are randomly generated from the total, and the combination of the two equals to the total overbooking numbers.
#### The different finance compensation to excess passengers who do not have a seat 
Based on the US policy, the compensation for bumped passengers varies according to the waiting time for changed flight schedule. There are three categories, for people who have waited within one hour, there is no compensation. For those who have waited for one to two hours and more than two hours, the compensations are $400 and $800 respectively. SO, we set the probability of no compensation to 60%, $400 to 30% and %800 to 10%.
#### The probability of no-show passengers who canceled the tickets before departure
For the cancellation, we randomly generate numbers from the number of no-show passengers, for those who cancelled before departure, there is a refund when computed the revenue of a flight.

## Hypothesis or hypotheses before running the simulation:
We assume a fixed air route, so the types of airplanes and the cost of each seat can be confirmed. 
The hypothesis is that within a certain range, the profits will grow following the overbooking numbers' increasement. Then there is a peak to achieve the maximum profits, however the profits will begin to drop after the peak as the overselling keep increasing due to the compensation for the excess passengers.

## Analytical Summary of your findings: (e.g. Did you adjust the scenario based on previous simulation outcomes?  What are the management decisions one could make from your simulation's output, etc.)?
The outputs of this program include a plot, a table and the optimizing result, which can show users how many tickets they should overbook to maximize the profit based on the certain flight type. These outputs prove that our hypothesis is right that overbooking tickets must be controlled in a fixed range or the company will lose revenue. In the fixed range, the largest overselling number can bring the highest revenue.

## Instructions on how to use the program:
The user will need to input the type of flight and other variables according to the reminder. And the program can compute how many tickets the airline should overbook to maximize the profit. For input variables like show up probability and the demand probability, we have provided a suggestion and of course the user can input these numbers according the statistics figure from the own situation. Moreover, we also create two files to demonstrate our result, including .py and .ipynb files. The reason why we create two files is that .py file can output different result of different airplane type with one whole code and .ipynb file is easier to read one result.

## All Sources Used:
Oberstone, J. L. (2010). Spreadsheet Simulation of Airline Reservation Policy Using Multimedia Software. International Journal of Advanced Corporate Learning (iJAC), 3(1). doi:10.3991/ijac.v3i1.1169

Basa, G., & Kedir, A. (2017). Modeling and optimization of the single-leg multi-fare class overbooking problem. Momona Ethiopian Journal of Science, 9(2), 200. doi:10.4314/mejs.v9i2.5
