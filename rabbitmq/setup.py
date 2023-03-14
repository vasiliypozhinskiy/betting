import setuptools

setuptools.setup(
    name="rabbitmq_clients",
    version="0.0.1",
    description="RabbitMQ publisher and consumer",
    packages=setuptools.find_packages(include=["rabbitmq_clients"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "backoff==2.2.1",
        "aio-pika==9.0.4",
        "pydantic==1.10.6",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
)
