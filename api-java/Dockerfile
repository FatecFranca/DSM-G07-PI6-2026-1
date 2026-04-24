FROM maven:3.9.6-eclipse-temurin-21 AS build

# Instala dependências para o MongoDB embarcado (Flapdoodle)
RUN apt-get update && apt-get install -y libssl-dev && rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x mvnw && ./mvnw clean package

FROM eclipse-temurin:21-jdk

WORKDIR /app

EXPOSE 8080

COPY --from=build /target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]