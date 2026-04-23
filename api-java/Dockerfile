FROM maven:3.9.6-eclipse-temurin-21 AS build

COPY . .

RUN ./mvnw clean package

FROM eclipse-temurin:21-jdk

WORKDIR /app

EXPOSE 8080

COPY --from=build /target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]