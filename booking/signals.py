from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Barber, Client

import json


@receiver(post_save, sender=Barber)
def schedule_init(sender, instance, created, **kwargs):
    if created:
        JSON_schedule_template = json.loads(instance.JSON_schedule_template)
        JSON_schedule_template["schedule_day"][0]["start"] = int(instance.start_time)
        JSON_schedule_template["schedule_day"][0]["end"] = int(instance.start_time) + 8
        instance.schedule = json.dumps(JSON_schedule_template)
        instance.save()

@receiver(post_save, sender=Client)
def schedule_update(sender, instance, created, **kwargs):
    if created:
        barber = Barber.objects.get(name = instance.barber)
        isValid = False

        # TEMPORARY
        if(instance.service == "HAIR"):
            creation_time = 1
        elif(instance.service == "WAX"):
            creation_time = 2
        else:
            creation_time = 2

        data = json.loads(barber.schedule)
        start_time = instance.start_time
        end_time = start_time + 1

        for i in range(len(data["schedule_day"]) - 1, -1, -1):
            if start_time >= data["schedule_day"][i]["start"]:
                if end_time <= data["schedule_day"][i]["end"]:
                    isValid = True
                    tmp_start = data["schedule_day"][i]["start"]
                    tmp_end = data["schedule_day"][i]["end"]
                    
                    '''
                    to avoid situation when tmp_start is equal to start_time and there is object next to him,
                    if there wasn't tmp_i, new data will apear after next object what will cause problems eg.
                    {start: 15, end:16}, {start:12, end: 14}
                    '''
                    tmp_i = i
                    
                    data["schedule_day"].pop(i)
                    if(tmp_start != start_time):
                        data["schedule_day"].insert(i, {
                            "start": tmp_start,
                            "end": start_time
                        })
                    else:
                        tmp_i -= 1

                    if(tmp_end != end_time):
                        data["schedule_day"].insert(tmp_i + 1 ,{
                            "start": end_time,
                            "end": tmp_end
                        })
        
        if(not isValid):
            raise Exception("Provided time doesn't match schedule")

        barber.schedule = json.dumps(data)
        barber.save()
        
