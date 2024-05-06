# QUESTIONS

1. Discuss your strategy and decisions implementing the application. Please, consider time complexity, effort cost, technologies used and any other variable that you understand important on your development process.

> Initially, my focus was on comprehending the provided documentation and understanding the necessary requirements. One of the outcomes of this process was the development of the database schema design. Despite the documentation suggesting that utilizing a database was optional, I opted to utilize SQLite to streamline development and showcase my proficiency in crafting queries.
> 
> The strategy I devised aimed at achieving the requirements in the simplest and most efficient manner possible. As the development progressed, I incorporated enhancements such as additional filters and stylistic improvements.
> 
> While the initial plan was to utilize both Django Rest Framework (DRF) and ReactJS, I concluded that this approach would contradict the principle of simplicity. Consequently, I decided to just use Django. Which compromised a more user-friendly organization of HTML and CSS codes.

2. How would you change your solution to account for future columns that might be requested, such as “Bill Voted On Date” or “Co-Sponsors”?

> Midway through the development process, I began contemplating new search filters. It was at this moment that I opted to separate certain fields that were initially combined into a single entity. This decision not only streamlined the development of new filters but also rendered the models more accommodating for potential future expansions.

3. How would you change your solution if instead of receiving CSVs of data, you were given a list of legislators or bills that you should generate a CSV for?

> An implementation I envision involves a page featuring a text field capable of receiving data, formatted with commas and line breaks, for instance. The user would input the data into the field and trigger the processing via a designated button. The insertion process across all tables would occur within a single transaction. Consequently, if any inconsistencies arise, the user would promptly receive notifications enabling them to rectify the errors. Alternatively, if the data adheres to the required standards, it would be promptly integrated into the database.

4. How long did you spend working on the assignment?

> I dedicated two hours to studying the requirements and devising strategies. Following this, I invested an additional hour and a half in testing various solutions I aimed to implement. Finally, I allocated three hours to the actual implementation of the code.
