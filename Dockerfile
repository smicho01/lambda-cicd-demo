FROM public.ecr.aws/lambda/python:3.13

RUN dnf upgrade -y --releasever=latest \
        rpm \
        rpm-libs \
        sqlite-libs \
    && dnf clean all

COPY lambda/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]
