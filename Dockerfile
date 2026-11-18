FROM public.ecr.aws/lambda/python:3.14

RUN dnf upgrade -y --releasever=latest \
        rpm \
        rpm-libs \
        sqlite-libs \
    && dnf clean all \
    && python -m pip uninstall -y pip

RUN rm -f /usr/local/bin/aws-lambda-rie

COPY lambda/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD ["lambda_function.lambda_handler"]
