class AudiobookModel:
    @staticmethod
    def check_field_presence(metadata):
        try:
            if (
                metadata["duration"] and metadata["name"] and
                metadata["author"] and metadata["narrator"]
            ):
                return True
        except KeyError:
            return False
    
    @staticmethod
    def check_duration(duration):
        if (isinstance(duration, int) and duration >= 0):
            return True
        return False
    
    @staticmethod
    def check_name(name):
        if (isinstance(name, str) and len(name) <= 100):
            return True
        return False

    @staticmethod
    def validate(metadata):
        are_fields_present = AudiobookModel.check_field_presence(metadata)
        if are_fields_present:
            if (
                AudiobookModel.check_name(metadata["name"]) and 
                AudiobookModel.check_name(metadata["author"]) and
                AudiobookModel.check_name(metadata["narrator"]) and
                AudiobookModel.check_duration(metadata["duration"])
            ):
                return True
        else:
            return False

