crTable_lapp = "CREATE TABLE IF NOT EXISTS Geshbank.loan_applications \
                (IdApp INT, \
                AppType VARCHAR(255), \
                Sex VARCHAR(10), \
                Age INT, \
                Education VARCHAR(255), \
                Job VARCHAR(255), \
                Experience INT, \
                AnnualIncome INT, \
                OtherSources INT, \
                BurdenRateBefore DOUBLE(10, 4), \
                Possessions VARCHAR(255), \
                CreditHistory VARCHAR(255), \
                AppSum INT, \
                Duration INT, \
                BurdenRateAfter DOUBLE(10, 4), \
                CreditScore DOUBLE(10, 4), \
                Category VARCHAR(255), \
                Approvement VARCHAR(255))"
crTable_la = "CREATE TABLE IF NOT EXISTS Geshbank.loan_accounts \
                (AccType VARCHAR(255), \
                ClientId INT, \
                IdApp INT, \
                BeginDate INT, \
                EndDate INT, \
                BeginQ INT, \
                EndQ DOUBLE(30, 2), \
                PD DOUBLE(10, 2), \
                LGD DOUBLE(10, 2), \
                InterestRate DOUBLE(10, 4), \
                Status VARCHAR(255), \
                Random DOUBLE(10, 4), \
                DefaultFunc DOUBLE(10, 4))"
crTable_da = "CREATE TABLE IF NOT EXISTS Geshbank.deposit_accounts \
                (AccType VARCHAR(255), \
                ClientId INT, \
                BeginDate INT, \
                EndDate INT, \
                BeginQ INT, \
                EndQ DOUBLE(30, 2), \
                Status VARCHAR(255))"
crTable_bf = "CREATE TABLE IF NOT EXISTS Geshbank.balance_frame \
                (DayNumber INT, \
                CashBalance DOUBLE(30, 2), \
                AssetBalance DOUBLE(30, 2), \
                DailyCashInflow DOUBLE(30, 2), \
                DailyCashOutflow DOUBLE(30, 2))"