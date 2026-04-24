FROM maven:3.9.6-eclipse-temurin-21 AS build

# Instala dependências e a biblioteca libssl1.1 (exigida pelo MongoDB embarcado)
RUN apt-get update && apt-get install -y wget && \
    wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    rm libssl1.1_1.1.1f-1ubuntu2_amd64.deb && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x mvnw && ./mvnw clean package

FROM eclipse-temurin:21-jdk

WORKDIR /app

EXPOSE 8080

COPY --from=build /target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]