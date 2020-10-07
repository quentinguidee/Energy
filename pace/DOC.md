# Wall

```xml
<building>
    <skin>
        <constructionElements>
            <!-- WALLTYPE -->
            <com.hemmis..Wall>
                ...
                <wallInstances>
                    <INITIAL>
                        WALL_INSTANCE
                    </INITIAL>               
                </wallInstances>
            </com.hemmis..Wall>
            <!-- ROOFTYPE -->
            <!-- FLOORTYPE -->
        </constructionElements>
        <wallPlanes>
            <INITIAL>
                WALL
            </INITIAL>
        </wallPlanes>
        <floorPlanes>
            ...
        </floorPlanes>
        <roofPlanes>
            <INITIAL>
                ROOF
            </INITIAL>
        </roofPlanes>
    </skin>
</building>
```

Since the WALL is placed after the wallInstance, we should register the wallInstances BEFORE the wall. Very handy...

Order :
* `wall_type.py`
* `wall_instance.py`
* `wall.py` inside the `wall_instance.py`

The structure looks like this...
```xml
<WallType> -> W-01
    <WallInstance> -> of type W-01
        <WallPlane> -> PARENT
            <WallInstance> -> of type W-02
                <WallType/> -> W-02
            </WallInstance>
            <WallInstance> -> of type W-03
                <WallType/> -> W-03
            </WallInstance>
        </WallPlane>
    </WallInstance>
</WallType>
```
Very convenient.

# Register (Layer 1)

## 1 wall with 1 instance

```python
pace_exporter.register(wall_type_1)
pace_exporter.register(wall_instance_1.inside_wall_type(wall_type_1))
pace_exporter.register(wall.inside_wall_instance(wall_instance_1))
```

## 1 wall with n instance

```python
pace_exporter.register(wall_type_1)
pace_exporter.register(wall_instance_1.inside_wall_type(wall_type_1))
pace_exporter.register(wall.inside_wall_instance(wall_instance_1))
pace_exporter.register(wall_instance_2.inside_wall(wall))
pace_exporter.register(wall_type_2.inside_wall_instance(wall_instance_2))
pace_exporter.register(wall_instance_n.inside_wall(wall))
pace_exporter.register(wall_type_n.inside_wall_instance(wall_instance_n))
```
