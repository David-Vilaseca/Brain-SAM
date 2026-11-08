# Brain-SAM 

<div align="center">
  <img src="https://github.com/panyinghong/Brain-SAM/blob/main/figures/model.png" width="1000">
</div>

## Installation 

- Create a virtual environment: `conda create -n brainsam python=3.10 -y` and `conda activate brainsam` 
- Install [PyTorch](https://pytorch.org/get-started/locally/): `torch==2.3.1` (choose the CUDA or CPU wheel for your machine)
- `git clone https://github.com/David-Vilaseca/Brain-SAM.git`
- cd Brain-SAM
- `pip install -e .`

The package includes all runtime dependencies used by training and inference.
The source directory is also registered as the package root, so imports such as
`modeling` and `dataset` work after installation.

On Windows, use `py -3` instead of `python` if that is how Python is registered.
Install PyTorch before the editable package, using the command generated for your
machine on the PyTorch website.

## Data Format
```python
npz = np.load('path to/brain_tumor.npz', allow_pickle=True)
imgs = npz['imgs'] # (D, W, H), [0, 255]
gts = npz['gts'] # (D, W, H), 3D tumor ground truth mask. 
```

## Training Brain-SAM
Training requires a CUDA-capable device, a pre-trained encoder checkpoint, and
the dataset directory. Run it from the source directory:

```bash
cd Brain-SAM
torchrun --standalone --nproc_per_node=2 train.py --data_prefix ../case --snapshot_path ../outputs --pretrain_weight path/to/encoder.pth --max_epoch 200 --rand_crop_size 128 --data_name brain --lr 6e-5 -bs 3
```

## Models
The model weights used in our experiments can be downloaded from this ([Baidu Netdisk](https://pan.baidu.com/s/1EhiJ1VxRvIVhahxmDeG5ng?pwd=ajrs)) link.
## Inference

Inference uses the attached full model checkpoint. Since large checkpoint files
are not stored in Git, copy it after cloning:

```bash
mkdir -p Brain-SAM/checkpoints
cp /path/to/model.pth Brain-SAM/checkpoints/model.pth
```

On Windows, the equivalent is:

```powershell
New-Item -ItemType Directory -Force .\Brain-SAM\checkpoints
Copy-Item C:\path\to\model.pth .\Brain-SAM\checkpoints\model.pth
```

If the checkpoint is stored elsewhere, pass its path explicitly.

Single-GPU / CPU:

```bash
python Brain-SAM/test.py --data_prefix case --checkpoint Brain-SAM/checkpoints/model.pth -bs 1
```

Multi-GPU (e.g., 2 GPUs with `torchrun`):

```bash
torchrun --standalone --nproc_per_node=2 Brain-SAM/test.py --data_prefix case --checkpoint Brain-SAM/checkpoints/model.pth -bs 1
```

Inference automatically uses CUDA when available and falls back to CPU. The
default test data is the included `case/` directory, and results are written to
`outputs/`.

### Batch Size (`-bs` / `--batch_size`)

- **`-bs 1` (Recommended for evaluation)**: Processes each 3D volume individually so that each case receives its own distinct row in `outputs/result/.../loss_results.csv`.
- **`-bs > 1` (Default: `2`)**: Batches multiple volumes together for higher inference throughput, though evaluation metrics in the output CSV will represent batch-level aggregations.
- **Multi-GPU inference with `torchrun`**: When running across multiple GPUs (e.g., `--nproc_per_node=2`), PyTorch's `DistributedSampler` distributes samples across ranks. If the number of cases is not evenly divisible by the number of GPUs, `DistributedSampler` pads the dataset with duplicate samples so all ranks process equal batch counts. For evaluating small sets of cases without duplicate entries, run on a single GPU with `-bs 1`.

## Major Results
Our results outperform the state-of-the-art methods in terms of both Dice and HD95.
<div align="center">
  <img src="https://github.com/panyinghong/Brain-SAM/blob/main/figures/result.png" width="2600">
</div>
