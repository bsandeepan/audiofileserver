class AudiobookModel:
    @staticmethod
    def check_field_presence(song_metadata):
        try:
            if (
                song_metadata["duration"] and song_metadata["name"] and
                song_metadata["author"] and song_metadata["narrator"]
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
    def validate(song_metadata):
        are_fields_present = AudiobookModel.check_field_presence(song_metadata)
        if are_fields_present:
            if (
                AudiobookModel.check_name(song_metadata["name"]) and 
                AudiobookModel.check_name(song_metadata["author"]) and
                AudiobookModel.check_name(song_metadata["narrator"]) and
                AudiobookModel.check_duration(song_metadata["duration"])
            ):
                return True
        else:
            return False

