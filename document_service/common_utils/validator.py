def validate_payload(func):
    def wrapper(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.payload = serializer.validated_data
        return func(self, request, *args, **kwargs)
    return wrapper
        