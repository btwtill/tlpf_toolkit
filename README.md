# Thanks

!!Huge thanks to CGMAs Mechanical Rigging Course Instructor Martin Louton and Tim Coleman to provide the underlying template for this Maya shelf!!
https://github.com/martinlanton/mechRig_toolkit

## Whats it For?

    Collection of Self Written or Inspired Maya Scripts to help make the rigging life easier!

**First shelf Install **

```python
from tlpf_toolkit.shelves import shelf_user_utils
import importlib
importlib.reload(shelf_user_utils)
shelf_user_utils.load(name="tlpf_shelf")
```

**userSetup.py - entry**

```python
    import maya.utils


    # ==========================================
    # Load Custom User Shelf at Maya startup
    # ==========================================

    from tlpf_toolkit.shelves import shelf_user_utils


    def load_user_shelf():
        shelf_user_utils.load(name="tlpf_shelf")


    maya.utils.executeDeferred("load_user_shelf()")
```