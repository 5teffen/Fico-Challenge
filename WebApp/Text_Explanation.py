
import pandas as pd
import numpy as np

def generate_text_explanation(per, sample, target, changes_vec , anchs_vec):
    # -- Assumes -9s are accounted for --
    text_string = "The model predicts that this client is "

    if (per > 0.5):
        text_string += "good"
    else:
        text_string += "bad"

    text_string += " with a score of " + "###" + "%\n\n"

    changes_lst = []
    anchs_lst = []

    # -- Create column lists --
    if (anchs_vec is not None):
        for an in range(len(anchs_vec)):
            if (anchs_vec[an] != 0):
                anchs_lst.append(an)
        text_string += anchs_text_exp(sample, anchs_lst, per)

    if (changes_vec is not None):
        for ch in range(len(changes_vec)):
            if (changes_vec[ch] != 0):
                changes_lst.append(ch)
        text_string += "\n\n"
        text_string += changes_text_exp(sample, target, changes_lst, per)

    # print(text_string)
    return text_string




def anchs_text_exp(sample, col_lst, per):

    # -- Writes the header line -- 
    if (per>0.5):
        explanation = "Key Features \nThe key factors that have contributed to the model's positive decision:"
    else:
        explanation = "Key Features \nThe key factors that have contributed to the model's negative decision:"

    for col in col_lst:


        # print(col)

        if (col == 0):
            name = " External Risk Estimate "
            val = str(sample[0])
            # Monotonicity Decreasing
            if (per>0.5):
                explanation += "\n - "+ "The high value for" + name
            else:
                explanation += "\n - "+ "The low value for" + name


        elif (col == 1):
            name = " Months Since Oldest Trade Open"
            # Monotonicity Decreasing
            val = str(sample[1])
            if (per>0.5): 
                explanation += "\n - "+ "A considerable period of " + val + " Months has passed Since Oldest Trade was Open."
            else: 
                explanation += "\n - "+ "Only " + val + " Months have passed Since Oldest Trade was Open."
        
        elif (col == 2):
            name = "Months Since Last Trade Open"
            # Monotonicity Decreasing
            val = str(sample[2])
            if (per>0.5):
                explanation += "\n - "+ "A considerable period of " + val + " Months have passed Since a Recent Trade was Open."
            else:
                explanation += "\n - "+ "Only " + val + " Months have passed Since a Recent Trade was Open."
        
        elif (col == 3):
            name = "Average Months in File"
            # Monotonicity Decreasing
            val = str(sample[3])
            if (per>0.5):
                explanation += "\n - "+ "The client has a high average of " + val + " Months in File."
            else:
                explanation += "\n - "+ "The client has only an average of " + val + " Months in File."

        elif (col == 4):
            name = "Satisfactory Trades"
            # Monotonicity Decreasing
            val = str(sample[4])
            if (per>0.5):
                explanation += "\n - "+ "The client has a high number of " + name 
            else:
                explanation += "\n - "+ "The client has a low number of " + name

        elif (col == 5):
            name = "Trades 60+ Ever"
            # Monotonicity Increasing
            val = str(sample[5])
            if (per>0.5):
                explanation += "\n - "+ "The client has very few trade lines for which payment was received 60 days past its due date"
            else:
                explanation += "\n - "+ "The client has too many trade lines for which payment was received 60 days past its due date"

            # WHAT IS THIS??!?
        elif (col == 6):
            name = "Trades 90+ Ever"
            # Monotonicity Increasing
            val = str(sample[6])
            if (per>0.5):
                explanation += "\n - "+ "The client has very few trade lines for which payment was received 90 days past its due date"
            else:
                explanation += "\n - "+ "The client has too many trade lines for which payment was received 90 days past its due date"
        elif (col == 7):
            name = "% Trades Never Delq."
            # Monotonicity Decreasing
            val = str(sample[7])
            if (per>0.5):
                explanation += "\n - "+ "This client has a overwhelming percentage of Trades that have Never gone Delinquent."
            else:
                explanation += "\n - "+ "This client has a alarmingly small percentage of Trades that have Never gone Delinquent."

        elif (col == 8):
            name = "Months Since Most Recent Delq."
            # Monotonicity Decreasing
            val = str(sample[8])
            if val == "150":
                explanation += "\n - "+ "This person has never been delinquent"
            else:
                if (per>0.5):
                    explanation += "\n - "+ val + " months have passed since Last Deliquency."
                else:
                    explanation += "\n - "+ "Only " + val + " Months have passed since Last Deliquency."
        elif (col == 9):
            name = "Max Delq. Last 12M"
            # Monotonicity Decreasing
            val = sample[9]
            if (val == 0):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client does not exist."
            elif (val == 1):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client is unknown."
            elif (val == 2):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months indicates a derogatory comment."
            elif (val == 3):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client is over 120 days."
            elif (val == 4):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client is over 90 days."
            elif (val == 5):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client is over 60 days."
            elif (val == 6):
                explanation += "\n - "+ "The Maximum Deliquency in the last 12 Months for this client is over 30 days."
            elif (val == 7):
                explanation += "\n - "+ "This client has not been delinqent in the past 12 months."

     
        elif (col == 10):
            name = "Max Delq. Ever"
            # Monotonicity Decreasing
            val = sample[10]

            if (val == 0):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client does not exist."
            elif (val == 1):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client is unknown."
            elif (val == 2):
                explanation += "\n - "+ "The Maximum Deliquency Ever indicates a derogatory comment."
            elif (val == 3):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client is over 120 days."
            elif (val == 4):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client is over 90 days."
            elif (val == 5):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client is over 60 days."
            elif (val == 6):
                explanation += "\n - "+ "The Maximum Deliquency Ever for this client is over 30 days."
            elif (val == 7):
                explanation += "\n - "+ "This client has never been delinqent."

        elif (col == 11):
            name = "Total Trades"
            # Monotonicity Unknown
            val = str(sample[11])
            if (per>0.5):
                explanation += "\n - "+ "The number of " + name + "is an important factor in the positive decision."
            else:
                explanation += "\n - "+ "The number of " + name + "is an important factor in the negative decision."
        elif (col == 12):
            name = "Trades Open Last 12M"
            # Monotonicity Increasing
            val = str(sample[12])
            if (per>0.5):
                explanation += "\n - "+ "The client has a Opened a very small number of trades in the past 12 Months."
            else:
                explanation += "\n - "+ "The client has a Opened a high number of trades in the past 12 Months."

        elif (col == 13):
            name = "% Installment Trades"
            # Monotonicity Unknown
            val = str(sample[13])
            explanation += "\n - "+ "The percentage of Installment Trades is an important feature for the model's decision"

        elif (col == 14):
            name = "Months Since Most Recent Inq"
            # Monotonicity Decreasing
            val = str(sample[14])
            if val == "150":
                explanation += "\n - "+ "No inquiries have been made against this person."
            if (per>0.5): 
                explanation += "\n - "+ val + " Months have passed since the most Recent Inquiry"
            else:
                explanation += "\n - "+ "Only " + val + " months have passed since the most Recent Inquiry"
        elif (col == 15):
            name = "Inq Last 6 Months"
            # Monotonicity Increasing
            val = str(sample[15])
            if (per>0.5):
                explanation += "\n - "+ "The client has only " + val + "inquiries in the Past 6 Months"
            else:
                explanation += "\n - "+ "The client has too many inquiries in the Past 6 Months"
        elif (col == 16):
            name = "Inq Last 6 Months exl. 7 days"
            # Monotonicity Increasing
            val = str(sample[16])
            if (per>0.5):
                explanation += "\n - "+ "The client has only " + val + "inquiries in the Past 6 Months when excluding the last 7 days"
            else:
                explanation += "\n - "+ "The client has too many inquiries in the Past 6 Months even when excluding the last 7 days"
        elif (col == 17):
            # print("enter")
            name =  "Revolving Burden"
            # Monotonicity Increasing
            val = str(sample[17])
            if (per>0.5):
                explanation += "\n - "+ "The client has a good ratio of revolving balance against their credit limit." 
            else:
                explanation += "\n - "+ "The client has a poor ratio of revolving balance against their credit limit." 
        elif (col == 18):
            name =  "Installment Burden"
            # Monotonicity Increasing
            val = str(sample[18])
            if (per>0.5):
                explanation += "\n - "+ "The client has maintained a good ratio for installment balance against their original loan amount." 
            else:
                explanation += "\n - "+ "The client has averaged a poor ratio for installment balance against their original loan amount." 
        elif (col == 19):
            name =  "Revolving Trades w/ Balance"
            # Monotonicity Unknown
            val = str(sample[19])
            explanation += "\n - "+ "The number of Revolving Trades with balance is " + val 
                   
        elif (col == 20):
            name =  "Installment Trades w/ Balance"
            # Monotonicity Unknown
            val = str(sample[20])
            explanation += "\n - "+ "The number of Revolving Trades with balance is " + val

        elif (col == 21):
            name =  "Bank Trades w/ High Utilization Ratio"
            # Monotonicity Increasing
            val = str(sample[21])
            if (per>0.5):
                explanation += "\n - "+ "Only a small number of Bank Trades have a High Utilization Ratio"
            else:
                explanation += "\n - "+ "Too many Bank Trades have a High Utilization Ratio"
        elif (col == 22):
            name = "% trades with balance"
            # Monotonicity Unknown
            val = str(sample[22])
            explanation += "\n - "+ "Maintained "+ val +" percentage of trades with balance"

    return explanation


def changes_text_exp(sample, target, col_lst, per):

    # -- Writes the header line -- 
    if (per<0.5):
        explanation = "Suggested Changes \nIf the client manages to make the following improvements the model would predict a positive decision:" 
    else:
        explanation = "Warnings \nIf the client's results fall for the following features the model would revert to a negative decision:" 
    
    # -- Hard coded text -- 
    for col in col_lst:
        if (col == 0):
            name = " External Risk Estimate "
            val = str(sample[0])
            tar = str(target[0])
            # Monotonicity Decreasing
            if (per>0.5):
                explanation += "\n - "+ "The External Risk Estimate should not fall to a value of " + tar +'.'
            else:
                explanation += "\n - "+ "The External Risk Estimate needs to be increased from " + val + " to " + tar +'.'


        elif (col == 1):
            name = " Months Since Oldest Trade Open"
            # Monotonicity Decreasing
            val = str(sample[1])
            tar = str(target[1])
            if (per>0.5): 
                explanation += "\n - "+ "The number of Months Since the Oldest Trade was Open should not fall below the " + tar + " mark."
            else: 
                explanation += "\n - "+ "This clients needs to wait such that " + tar + " Months will have passed since the Oldest Trade was Open."
        
        elif (col == 2):
            name = "Months Since Last Trade Open"
            # Monotonicity Decreasing
            val = str(sample[2])
            tar = str(target[2])
            if (per>0.5): 
                explanation += "\n - "+ "The number of Months Since the Most Recent Trade was Open should not fall below the " + tar + " mark."
            else: 
                explanation += "\n - "+ "This client needs to wait such that " + tar + " Months will have passed since the Most Recent Trade was Open."
        
        elif (col == 3):
            name = "Average Months in File"
            # Monotonicity Decreasing
            val = str(sample[3])
            tar = str(target[3])
            if (per>0.5):
                explanation += "\n - "+ "The client's Average number of Months in File should not be less than " + tar +'.'
            else:
                explanation += "\n - "+ "This client needs to wait such that their Average Months in File increases to " + tar +'.'

        elif (col == 4):
            name = "Satisfactory Trades"
            # Monotonicity Decreasing
            val = str(sample[4])
            tar = str(target[4])
            if (per>0.5):
                explanation += "\n - "+ "The client should maintain a number of Satisfactory Trades that exceeds the " + tar + " threshold."
            else:
                explanation += "\n - "+ "The client needs to increase the number of Satisfactory Trades from " + val + " to " +" " + tar +'.'

        elif (col == 5):
            name = "Trades 60+ Ever"
            # Monotonicity Increasing
            val = str(sample[5])
            tar = str(target[5])
            if (per>0.5):
                explanation += "\n - "+ "The number of trade lines for which payment was received 60 days past should not increase past the " + tar + " threshold."
            else:
                explanation += "\n - "+ "The number of trade lines for which payment was received 60 days past needs to be decreased to below the " + tar + " threshold."

            # WHAT IS THIS??!?
        elif (col == 6):
            name = "Trades 90+ Ever"
            # Monotonicity Increasing
            val = str(sample[6])
            tar = str(target[6])
            if (per>0.5):
                explanation += "\n - "+ "The number of trade lines for which payment was received 90 days past should not increase past the " + tar + " threshold."
            else:
                explanation += "\n - "+ "The number of trade lines for which payment was received 90 days past needs to be decreased to below the " + tar + " threshold."
        
        elif (col == 7):
            name = "% Trades Never Delq."
            # Monotonicity Decreasing
            val = str(sample[7])
            tar = str(target[7])
            if (per>0.5):
                explanation += "\n - "+ "The percentage of Trades that have never gone Delinquent needs to remain above " + tar + " percent."
            else:
                explanation += "\n - "+ "The percentage of Trades that have never gone Delinquent should be improved to approximately " + tar + " percent."

        elif (col == 8):
            name = "Months Since Most Recent Delq."
            # Monotonicity Decreasing
            val = str(sample[8])
            tar = str(target[8])
            change = str(target[8]-sample[8])

            if (per>0.5):
                explanation += "\n - "+ "The client needs to ensure that a situation where only " + tar + " months have passed since Last Deliquency doesn't arise."
            else:
                explanation += "\n - "+ "The client needs to wait " + change + " months such that a total of " + tar + " Months have passed since Last Deliquency."

        elif (col == 11):
            name = "Total Trades"
            # Monotonicity Unknown
            val = str(sample[11])
            tar = str(target[11])
            if (per>0.5):
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client should maintain a number of Total Trades that exceeds the " + tar + " threshold."
                else:
                    explanation += "\n - "+ "The client should maintain a number of Total Trades that falls below the " + tar + " threshold."
            else:
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client needs to increase the number of Total Trades from " + val + " to " + tar +'.'
                else:
                    explanation += "\n - "+ "The client needs to decrease the number of Total Trades from " + val + " to " + tar +'.'


        elif (col == 12):
            name = "Trades Open Last 12M"
            # Monotonicity Increasing
            val = str(sample[12])
            tar = str(target[12])
            if (per>0.5):
                explanation += "\n - "+ "The number of Trades Open in the past 12M should not exceed " + tar + '.'
            else:
                explanation += "\n - "+ "The number of Trades Open in the past 12M should be decreased to below the " + tar + 'threshold.'

        elif (col == 13):
            name = "% Installment Trades"
            # Monotonicity Unknown
            val = str(sample[13])
            tar = str(target[13])

            if (per>0.5):
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client should maintain a percentage of Installment Trades that exceeds the " + tar + " percent threshold."
                else:
                    explanation += "\n - "+ "The client should maintain a percentage of Installment Trades that falls below the " + tar + " percent threshold."
            else:
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client needs to increase the percentage of Installment Trades from " + val + " to " + tar +'.'
                else:
                    explanation += "\n - "+ "The client needs to decrease the percentage of Installment Trades from " + val + " to " + tar +'.'

        elif (col == 14):
            name = "Months Since Most Recent Inq"
            # Monotonicity Decreasing
            val = str(sample[14])
            tar = str(target[14])
            change = str(target[14]-sample[14])

            if (per>0.5):
                explanation += "\n - "+ val + " Months have passed since the most Recent Inquiry"
            else:
                explanation += "\n - "+ "Only " + val + " months have passed since the most Recent Inquiry"
        elif (col == 15):
            name = "Inq Last 6 Months"
            # Monotonicity Increasing
            val = str(sample[15])
            tar = str(target[15])
            if (per>0.5):
                explanation += "\n - "+ "The client should maintain fewer than " + tar + " inquiries in the Past 6 Months."
            else:
                explanation += "\n - "+ "The client needs to have fewer than " + tar + " inquiries in the Past 6 Months."
        elif (col == 16):
            name = "Inq Last 6 Months exl. 7 days"
            # Monotonicity Increasing
            val = str(sample[16])
            tar = str(target[16])
            if (per>0.5):
                explanation += "\n - "+ "The client should maintain fewer than " + tar + " inquiries in the Past 6 Months when excluding that past 7 days."
            else:
                explanation += "\n - "+ "The client needs to have fewer than " + tar + " inquiries in the Past 6 Months when excluding that past 7 days."
        elif (col == 17):
            name =  "Revolving Burden"
            # Monotonicity Increasing
            val = str(sample[17])
            tar = str(target[17])
            if (per>0.5):
                explanation += "\n - "+ "The client should maintain a low Revolving Burden of less than " + tar + '.'
            else:
                explanation += "\n - "+ "The client needs to decrease their relatively high Revolving Burden to less than " + tar + '.'
        elif (col == 18):
            name =  "Installment Burden"
            # Monotonicity Increasing
            val = str(sample[18])
            tar = str(target[18])
            if (per>0.5):
                explanation += "\n - "+ "The client should maintain a low Revolving Burden of less than " + tar + '.'
            else:
                explanation += "\n - "+ "The client needs to decrease their relatively high Revolving Burden to less than " + tar + '.'

        elif (col == 19):
            name =  "Revolving Trades w/ Balance"
            # Monotonicity Unknown
            val = str(sample[19])
            tar = str(target[19])

            if (per>0.5):
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client should maintain a number of Revolving Trades with Balance such that it exceeds the " + tar + " threshold."
                else:
                    explanation += "\n - "+ "The client should maintain a number of Revolving Trades with Balance such that it stays below the " + tar + " threshold."
            else:
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The number of Revolving Trades with Balance needs to be increased from  " + val + " to " +" " + tar +'.'
                else:
                    explanation += "\n - "+ "The number of Revolving Trades with Balance needs to be decreased from  " + val + " to " +" " + tar +'.'
            
                   
        elif (col == 20):
            name =  "Installment Trades w/ Balance"
            # Monotonicity Unknown
            val = str(sample[20])
            tar = str(target[20])
            explanation += "\n - "+ "The number of Revolving Trades with balance is " + val


            if (per>0.5):
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client should maintain a number of Installment Trades with Balance such that it exceeds the " + tar + " threshold."
                else:
                    explanation += "\n - "+ "The client should maintain a number of Installment Trades with Balance such that it stays below the " + tar + " threshold."
            else:
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The number of Installment Trades with Balance needs to be increased from  " + val + " to " +" " + tar +'.'
                else:
                    explanation += "\n - "+ "The number of Installment Trades with Balance needs to be decreased from  " + val + " to " +" " + tar +'.'

        elif (col == 21):
            name =  "Bank Trades w/ High Utilization Ratio"
            # Monotonicity Increasing
            val = str(sample[21])
            tar = str(target[21])
            if (per>0.5):
                explanation += "\n - "+ "The small number of Bank Trades that have a High Utilization Ratio should be maintained below " + tar + '.'
            else:
                explanation += "\n - "+ "The high number of Bank Trades that have a High Utilization Ratio has to be decreased below the " + tar + ' mark.'
        elif (col == 22):
            name = "% Trades with balance"
            # Monotonicity Unknown
            val = str(sample[22])
            tar = str(target[22])
            if (per>0.5):
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The percentage of Trades with Balance needs to stay below the " + tar + " percent threshold."
                else:
                    explanation += "\n - "+ "The percentage of Trades with Balance needs to stay above the " + tar + " percent threshold."
            else:
                if (int(tar) < int(val)):
                    explanation += "\n - "+ "The client needs to increase the percentage of Trades that have a balance from " + val + " to " + tar +'.'
                else:
                    explanation += "\n - "+ "The client needs to increase the percentage of Trades that have a balance from " + val + " to " + tar +'.'

    return explanation
    








