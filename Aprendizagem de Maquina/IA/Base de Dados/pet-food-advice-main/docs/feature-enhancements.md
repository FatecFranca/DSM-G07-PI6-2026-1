---
outline: deep
---

# Feature Enhancements

**Every project can be improved.** As technology professionals, we need to know the time to stop because, in the business world, we are ruled by the project trio: scope, cost and time. This section shows some ideas to improve or place this feature in a real production environment.

## Frontend

1. **Click anywhere out the sidebar to close it.** As well when changing the route.

2. **Control the form steps using the URL.** Besides, it's a simple feature. I'd prefer to use the router to control the steps for dense forms because it's easier to share the URL with someone, navigate using the browser arrows, or go to any desired page.

3. **Save the already recommended products on the database.** It's a good idea to avoid recommending different products, as that could confuse the user. Also, in a real scenario, the user would go back to this feature to check what was recommended previously instead of making the flow again.

4. **Use veterinarians to improve the recommendation.** We can develop a feature for the veterinarians to approve or disapprove the recommendation made for the specific pet. This information won't be shown to the pet owner, but we can use that data to improve the algorithm.

5. **Store the user data in the localStorage.** This is the default approach in a real scenario after authenticating the user. The `userStore` must search user data in the localStorage before going to a sign-in/sign-up route and proceeding with the API call for each case.

6. **Error component to show a message when the API is down.**

7. **Calculate the recommended food amount.** The API can return the recommended amount of food for the pet based on the weight and the food characteristics such as calories.

8. **Give tips about dividing the food amount throughout the day.** The front end can show a draw with different arrangements of food portions. For example, if the recommended amount is 100g, the user can divide it into two meals of 50g or three meals of 33g. Another tip we can show is to use a scale to measure the food amount at the beginning of the day and put it in a container to avoid over or under-feeding the pet.

9. **Use all icons in SVG format.** It's a good practice to use SVG icons instead of PNG or JPG because they are smaller and can be scaled without losing quality. For the conditions icons, I used PNG because I downloaded them from Flaticon, and SVG is paid.

## Backend

1. **Use a real database solution to store the data.** I suggest a NoSQL database because the food objects can change and gain different attributes over time, as it's not a core feature and managing a relational database would consume a lot of time.

2. **Move the endpoint for an existing API.** As proof of concept, a serveless solution achieves the goal. It'd put it in an Vetster's existent API. Maintaining the same codebase, authentication, and deployment process is better.

3. **Change the dataset to use brands and products that Vetster wants to work with.**

4. **Use types to improve API reliability.**

5. **Use a cache solution to improve the API performance.** The cache can be used to store the results of the most common requests.
