FROM registry.access.redhat.com/ubi8/openjdk-11

# Copy the JMX exporter jar into the image
COPY jmx_prometheus_javaagent.jar /jmx_prometheus_javaagent.jar

# Set working directory
WORKDIR /

# Entrypoint is not needed; the Kafka container will just use this image to copy the jar
