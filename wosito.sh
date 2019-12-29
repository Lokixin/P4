FEAT=$1
itnum=$2
itnum2=$(($itnum - 1))
file_name=results/prueba1.txt
file_name2=results/prueba2.txt
file_name3=results/errcostval.txt
file_name4=results/gauss.txt
file_name5=results/gaussworld.txt
declare -a arr
declare -a params
outpy=$(python3 scripts/enjambre.py 0 $itnum 12 25)
arr=($(echo "$outpy" | tr ' ' '\n'))
for i in $(seq 0 $itnum2)
do
    for coeffidx in $(seq 0 $itnum2)
    do
        run_spkid $FEAT ${arr[$coeffidx]} 12 12 24 
        FEAT=$FEAT run_spkid train 12 12 12 24 
        FEAT=$FEAT run_spkid test
        FEAT=$FEAT run_spkid classerr | tee $file_name 
        FEAT=$FEAT run_spkid trainworld 12 12 12 24 
        FEAT=$FEAT run_spkid verify
        FEAT=$FEAT run_spkid verif_err | tee -a $file_name
        errAndCost=$(python3 scripts/errAndCost.py)
        params=($(echo "$errAndCost" | tr ' ' '\n'))
        arr=($(echo "$outpy" | tr ' ' '\n'))
        echo "${params[0]} ${params[1]}" >>"$file_name2"
        echo "${params[0]} ${params[1]} ${arr[$coeffidx]}" >>"$file_name3"
    done
    outpy=$(python3 scripts/enjambre.py 1 $itnum 12 25)
    arr=($(echo "$outpy" | tr ' ' '\n'))
    rm $file_name2
done

numcoefs=$(python3 scripts/bestone.py $file_name3)
echo "valor = $numcoefs"
rm scripts/values.npy scripts/speed.npy scripts/costs.npy

outpy=$(python3 scripts/enjambre.py 0 $itnum 12 64)
arr=($(echo "$outpy" | tr ' ' '\n'))
for i in $(seq 0 $itnum2)
do
    for coeffidx in $(seq 0 $itnum2)
    do
        run_spkid $FEAT $numcoefs ${arr[$coeffidx]} 12 24 
        FEAT=$FEAT run_spkid train $numcoefs ${arr[$coeffidx]} 12 24 
        FEAT=$FEAT run_spkid test
        FEAT=$FEAT run_spkid classerr | tee $file_name 
        FEAT=$FEAT run_spkid trainworld $numcoefs 12 12 24 
        FEAT=$FEAT run_spkid verify
        FEAT=$FEAT run_spkid verif_err | tee -a $file_name
        errAndCost=$(python3 scripts/errAndCost.py)
        params=($(echo "$errAndCost" | tr ' ' '\n'))
        arr=($(echo "$outpy" | tr ' ' '\n'))
        echo "${params[0]} ${params[1]}" >>"$file_name2"
        echo "${params[0]} ${params[1]} ${arr[$coeffidx]}" >>"$file_name4"
    done
    outpy=$(python3 scripts/enjambre.py 1 $itnum 12 64)
    arr=($(echo "$outpy" | tr ' ' '\n'))
    rm $file_name2
done

numgauss=$(python3 scripts/bestone.py $file_name4)
rm scripts/values.npy scripts/speed.npy scripts/costs.npy

outpy=$(python3 scripts/enjambre.py 0 $itnum 12 64)
arr=($(echo "$outpy" | tr ' ' '\n'))
for i in $(seq 0 $itnum2)
do
    for coeffidx in $(seq 0 $itnum2)
    do
        run_spkid $FEAT $numcoefs $numgauss ${arr[$coeffidx]} 24 
        FEAT=$FEAT run_spkid train $numcoefs $numgauss ${arr[$coeffidx]} 24  
        FEAT=$FEAT run_spkid test
        FEAT=$FEAT run_spkid classerr | tee $file_name 
        FEAT=$FEAT run_spkid trainworld $numcoefs $numgauss ${arr[$coeffidx]} 24 
        FEAT=$FEAT run_spkid verify
        FEAT=$FEAT run_spkid verif_err | tee -a $file_name
        errAndCost=$(python3 scripts/errAndCost.py) 
        params=($(echo "$errAndCost" | tr ' ' '\n'))
        arr=($(echo "$outpy" | tr ' ' '\n'))
        echo "${params[0]} ${params[1]}" >>"$file_name2"
        echo "${params[0]} ${params[1]} ${arr[$coeffidx]}" >>"$file_name5"
    done
    outpy=$(python3 scripts/enjambre.py 1 $itnum 12 64)
    arr=($(echo "$outpy" | tr ' ' '\n'))
    rm $file_name2
done

numgaussworld=$(python3 scripts/bestone.py $file_name5)
python3 scripts/damsndMSG.py
